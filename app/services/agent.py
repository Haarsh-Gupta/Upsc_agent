import os
import base64
import mimetypes
from typing import List, Dict
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate


from app.prompts.ocr_prompt import ocr_prompt , ocr_parser
from app.prompts.evaluation_prompt import evaluation_prompt , evaluation_parser
from app.prompts.Gs_rubric_prompt import gs1_text , gs2_text , gs3_text

GS_prompt = {"GS1" : gs1_text,
             "GS2" : gs2_text,
             "GS3" : gs3_text}


import os
import mimetypes

class AnswerEvaluation:

    def __init__(self, total_marks: int, subject: str , flash_model, pro_model):
        self.flash_model = flash_model
        self.pro_model = pro_model
        
        if total_marks not in [10, 15, 20]:
            raise ValueError("Marks must be 10, 15, or 20")
        self.total_marks = total_marks

        if subject not in ["GS1", "GS2", "GS3"]:
            raise ValueError("Subject must be GS1, GS2, or GS3")
        self.subject = subject 

    def prepare_content(self, files_path: List[str]):
        """Helper to create the image/pdf payload"""
        content_blocks = [
            {"type": "text", "text": ocr_prompt.format()}
        ]

        for path in files_path:
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")
            
            
            mime_type, _ = mimetypes.guess_type(path)
            if mime_type is None:
                if path.lower().endswith(('.jpg', '.jpeg')): mime_type = 'image/jpeg' 
                elif path.lower().endswith('.png'): mime_type = 'image/png'
                else: mime_type = 'application/octet-stream' 

            # 2. Encode
            with open(path, 'rb') as f:
                file_bytes = f.read()
                base64_data = base64.b64encode(file_bytes).decode("utf-8")

            # 3. Append to list
            content_blocks.append({
                "type": "media",
                "file_uri": None,
                "data": base64_data,
                "mime_type": mime_type
            })

        return content_blocks
        
    def ocr(self, files_path: List[str]):
        """Extracts text and question from images"""
        print("Running OCR...")
        message_content = self.prepare_content(files_path)

        if len(message_content) > 1:
            msg = HumanMessage(content=message_content)

            try:
                response = self.flash_model.invoke([msg])
                parsed_output = ocr_parser.parse(response.content)
                return parsed_output
            except Exception as e:
                print(f"OCR Error: {e}")
                return None
        else:
            print("No valid files to process.")
            return None

    def keypoint_generator(self, question: str):
        """Generates the marking scheme"""
        print("Generating Rubric...")
        prompt = PromptTemplate(
            template=GS_prompt[self.subject] + "\n\n {format_instructions}",
            input_variables=['question', 'total_marks'],
            partial_variables={'format_instructions': evaluation_parser.get_format_instructions()}
        )


        chain = prompt | self.flash_model | evaluation_parser
        res = chain.invoke({'question': question, 'total_marks': self.total_marks})
        return res

    def feedback(self, structure: Dict, answer: str):
        """Generates the final evaluation"""
        print("Evaluating Answer...")
        chain = evaluation_prompt | self.flash_model | evaluation_parser
        
        # # Convert structure to string for the prompt context
        # structure_str = json.dumps(structure)
        
        res = chain.invoke({'model_structure': structure, 'answer': answer})
        return res

    def full_evaluation(self, file_paths: List[str]):
        """Orchestrates the entire pipeline"""
        
        # Step 1: OCR
        ocr_result = self.ocr(file_paths)
        if not ocr_result: return "OCR Failed"
        
        student_question = ocr_result['question']
        student_answer = ocr_result['answer']
        
        # Step 2: Generate Rubric
        rubric = self.keypoint_generator(student_question)
        
        # Step 3: Evaluate
        final_feedback = self.feedback(rubric, student_answer)
        
        # return final_feedback
        return {'ocr_res' : ocr_result,
                'rubric_res' : rubric,
                'feedback_res' : final_feedback}
