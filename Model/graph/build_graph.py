from graph.state_graph import StateNode
from states.ocr_state import ocr_state
from states.human_state import human_state
from states.keypoint_state import keypoint_state
from states.rag_state import rag_state
from states.essay_state import essay_state
from states.evaluator_state import evaluator_state
from states.end_state import end_state

def build_pipeline_graph():
    OCR = StateNode("ocr", ocr_state)
    HUMAN = StateNode("human", human_state)
    KP = StateNode("keypoints", keypoint_state)
    RAG = StateNode("rag", rag_state)
    ESSAY = StateNode("essay", essay_state)
    EVAL = StateNode("evaluate", evaluator_state)
    END = StateNode("end", end_state)

    OCR.connect("human", HUMAN)
    HUMAN.connect("keypoints", KP)
    KP.connect("rag", RAG)
    RAG.connect("essay", ESSAY)
    ESSAY.connect("evaluate", EVAL)
    EVAL.connect("end", END)

    return OCR
