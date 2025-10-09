import streamlit as st
from langchain_groq import ChatGroq


@st.cache_resource
def initializeLLM():
    groq_api_key = st.secrets["GROQ_API_KEY"]

    # Initialize the Groq LLM
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.1-8b-instant"
    )

    return llm


def generate(prompt):
   #Generate text using Groq API.

    llm = initializeLLM()
    
    response = llm.invoke(prompt) # ChatGroq returns a string

    # Extract text first
    if hasattr(response, "content"):
        q = response.content
    else:
        q = str(response)
    # Then cleanup like before
    q = q.strip().splitlines()[0].strip()
    return q 

# === Disorders definitions (kept from your original) ===
disorders = {
    "Depression": {
        "core": [
            "Feeling down, depressed, or hopeless",
            "Little interest or pleasure in doing things",
            "Trouble falling or staying asleep or sleeping too much",
            "Feeling tired or having little energy"
        ],
        "extended": [
            "Poor appetite or overeating",
            "Feeling bad about yourself or feeling like a failure or have let yourself or your family down",
            "Trouble concentrating on things such as reading the newspaper or watching television",
            "Moving or speaking so slowly that other people could have noticed?   Or the opposite—being so fidgety or restless that you have been moving around a lot more than usual ",
            "Thoughts that you would be better off dead or of hurting yourself in some way "
        ]
    },
    "Anxiety": {
        "core": [
            "felt moments of sudden terror, fear, or fright",
            "felt anxious, worried, or nervous",
            "had thoughts of bad things happening, such as family tragedy, ill health, loss of a job, or accidents ",
            "felt a racing heart, sweaty, trouble breathing, faint, or shaky",
            "felt tense muscles, felt on edge or restless, or had trouble relaxing or trouble sleeping"
        ],
        "extended": [
            "avoided, or did not approach or enter, situations about which I worry",
            "left situations early or participated only minimally due to worries ",
            "spent lots of time making decisions, putting off making decisions, or preparing for situations, due to worries "
        ]
    },
    "PTSD": {
        "core": [
            "Having flashbacks, that is, you suddenly acted or felt as if a stressful experience from the past was happening all over again (for example, you reexperienced parts of a stressful experience by seeing, hearing, smelling, or physically feeling parts of the experience)? ",
            "Feeling very emotionally upset when something reminded you of a stressful experience? ",
            "Trying to avoid thoughts, feelings, or physical sensations that reminded you of a stressful experience? ",
            "Thinking that a stressful event happened because you or someone else (who didn’t directly harm you) did something wrong or didn’t do everything possible to prevent it, or because of something about you? ",
            "Having a very negative emotional state (for example, you were experiencing lots of fear, anger, guilt, shame, or horror) after a stressful experience? "
        ],
        "extended": [
            "Losing interest in activities you used to enjoy before having a stressful experience? ",
            "Being “super alert,” on guard, or constantly on the lookout for danger? ",
            "Feeling jumpy or easily startled when you hear an unexpected noise? ",
            "Being extremely irritable or angry to the point where you yelled at other people, got into fights, or destroyed things? ",
            "sought reassurance from others due to worries",
            "needed help to cope with anxiety (e.g., alcohol or medication, superstitious objects, or other people) "
        ]
    },
    "Panic Disorder": {
        "core": [
            "felt moments of sudden terror, fear or fright, sometimes out of the blue (i.e., a panic attack) ",
            "felt anxious, worried, or nervous about having more panic attacks ",
            "had thoughts of losing control, dying, going crazy, or other bad things happening because of panic attacks ",
            "felt a racing heart, sweaty, trouble breathing, faint, or shaky",
            "felt tense muscles, felt on edge or restless, or had trouble relaxing or trouble sleeping "
        ],
        "extended": [
            "avoided, or did not approach or enter, situations in which panic attacks might occur ",
            "left situations early, or participated only minimally, because of panic attacks ",
            "spent a lot of time preparing for, or procrastinating about (putting off), situations in which panic attacks might occur ",
            "distracted myself to avoid thinking about panic attacks ",
            "needed help to cope with panic attacks (e.g., alcohol or medication, superstitious objects,  other people) "
        ]
    }
}


def make_prompt_for_symptom(disorder: str, symptom: str, age: int, sex: str) -> str:
    """
    Build the system/user prompt to ask the LLM to generate a single scenario-based question.
    The prompt is adapted from your original, but kept safe and constrained.
    """
    prompt = (
        "<|start_header_id|>user<|end_header_id|>"
        "You are a clinical psychologist generating a patient questionnaire item.\n\n"
        "Disorder: {disorder}\n"
        "Symptom: {symptom}\n"
        "Age: {age}\n"
        "Sex: {sex}\n\n"
        "Your task: Write exactly ONE scenario-based question that relates to the symptom "
        "of the disorder and feels natural for the patient’s age and sex. The question must be "
        "Rules:\n"
        "The question can be answered by never, occasionally, sometimes, all the time "
        "Output only the question text.\n"
        "Do not include answers, code, or explanations."
        "Output ONLY ONE QUESTION"
        "NO OUTPUT OTHER THAN THE QUESTION"
        "<|end_header_id|>"
        "<|start_header_id|>psychologist<|end_header_id|>"
    )
    return prompt.format(disorder=disorder, symptom=symptom, age=age, sex=sex)


def ask_question_llm(disorder: str, symptom: str, age: int, sex: str, use_llm: bool = True) -> str:
    """
    Return the question text. If use_llm=True it will call your generate() function.
    For faster dev you can set use_llm=False and return a template string.
    """
    if not use_llm:
        return f"For {disorder}, how often do you experience: {symptom}?"
    prompt = make_prompt_for_symptom(disorder, symptom, age, sex)
    try:
        print("Sending prompt to LLM:", prompt)  # debug
        q = generate(prompt)
        print("LLM returned:", q)  # debug

        return q
    except Exception as e:
        # On any LLM issue, fallback to a safe template question
        print("LLM failed:", e)  # debug
        return f"For {disorder}, how often do you experience: {symptom}?"


# === Assessment session class ===
import json
from typing import Optional, Dict, Any


class AssessmentSession:
    """
    Stateful session object for one patient's assessment.
    Use get_next_question() to fetch the next question (no printing).
    Use submit_answer(score) to submit a 0-4 integer answer for the last returned question.
    When get_next_question() returns {'done': True}, call get_results() to retrieve final metrics.
    """

    def __init__(self, disorders_map: Dict[str, Dict[str, list]], age: int, sex: str, use_llm: bool = True):
        self.disorders_map = disorders_map
        self.disorder_names = list(disorders_map.keys())
        self.age = age
        self.sex = sex
        self.use_llm = use_llm

        # session state
        self.current_disorder_index = 0
        self.current_stage = "core"  # 'core' or 'extended'
        self.current_symptom_index = 0
        self.scores = {d: [] for d in self.disorder_names}
        self.last_question = None  # stores (disorder, symptom) for which we expect a response
        self.completed = False

    # ----- navigation helpers -----
    def _current_disorder(self) -> Optional[str]:
        if self.current_disorder_index >= len(self.disorder_names):
            return None
        return self.disorder_names[self.current_disorder_index]

    def _symptoms_for_current_stage(self):
        disorder = self._current_disorder()
        if disorder is None:
            return []
        return self.disorders_map[disorder][self.current_stage]

    # ----- core API -----
    def get_next_question(self) -> Dict[str, Any]:
        """
        Returns a dict describing the next question or completion state.
        Example return values:
          {"done": False, "disorder": "...", "symptom": "...", "question": "..."}
          {"done": True}
        """

        # If already done
        if self.completed or self.current_disorder_index >= len(self.disorder_names):
            self.completed = True
            return {"done": True}

        disorder = self._current_disorder()
        symptoms = self._symptoms_for_current_stage()

        # If we've exhausted the symptoms in this stage
        if self.current_symptom_index >= len(symptoms):
            # If just finished core, decide whether to move to extended or skip
            if self.current_stage == "core":
                core_scores = self.scores[disorder]  # these are only core scores at this point
                # decision rule: if >=2 items scored >= 2 (moderate/above), ask extended
                if sum(1 for s in core_scores if s >= 2) >= 2:
                    self.current_stage = "extended"
                    self.current_symptom_index = 0
                    return self.get_next_question()
                else:
                    # skip extended, move to next disorder
                    self.current_disorder_index += 1
                    self.current_stage = "core"
                    self.current_symptom_index = 0
                    return self.get_next_question()
            else:
                # finished extended stage — move to next disorder
                self.current_disorder_index += 1
                self.current_stage = "core"
                self.current_symptom_index = 0
                return self.get_next_question()

        # Return the next question
        symptom = symptoms[self.current_symptom_index]
        question_text = ask_question_llm(disorder, symptom, self.age, self.sex, use_llm=self.use_llm)

        # Save the last_question so submit_answer knows where to attach the score
        self.last_question = {"disorder": disorder, "symptom": symptom, "stage": self.current_stage, "index": self.current_symptom_index}

        return {
            "done": False,
            "disorder": disorder,
            "stage": self.current_stage,
            "symptom": symptom,
            "question": question_text
        }

    def submit_answer(self, score: int) -> None:
        """
        Submit an integer score for the last returned question.
        Score MUST be an int in 0..4. Returns the next question (same format as get_next_question()).
        """
        if self.last_question is None:
            raise RuntimeError("No outstanding question to answer. Call get_next_question() first.")

        # Validate score
        if not isinstance(score, int) or score < 0 or score > 4:
            raise ValueError("Score must be an integer between 0 and 4 inclusive.")

        disorder = self.last_question["disorder"]
        # Append the score to the disorder's scores
        self.scores[disorder].append(score)

        # Advance symptom index
        self.current_symptom_index += 1
        self.last_question = None


    def get_results(self) -> Dict[str, Dict[str, Any]]:
        """
        Compute final results for all disorders that have any scores.
        Returns a dict: disorder -> {raw_score, normalized (0-100), severity_code, severity_label}
        """
        results = {}
        for disorder in self.disorder_names:
            scores = self.scores.get(disorder, [])
            raw = sum(scores)

            full_max = (len(self.disorders_map[disorder]["core"]) + len(self.disorders_map[disorder]["extended"])) * 4
            normalized = (raw / full_max) * 100 if full_max > 0 else 0.0
            severity_code, severity_label = self._map_severity_from_percentage(normalized)

            results[disorder] = {
                "raw_score": raw,
                "normalized_pct": round(normalized, 2),
                "severity_code": severity_code,
                "severity_label": severity_label
            }
        return results

    def _map_severity_from_percentage(self, pct: float):
        """
        Map normalized percentage (0-100) to severity code and label.
        You can tune thresholds as desired.
        """
        if pct < 20:
            return 0, "Normal"
        elif pct < 40:
            return 1, "Mild"
        elif pct < 60:
            return 2, "Moderate"
        elif pct < 80:
            return 3, "Severe"
        else:
            return 4, "Extreme"

    # ----- serialization helpers ----- FOR NOW NOT IMPORTANT
    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable snapshot of session state (store this in DB/session)."""
        return {
            "age": self.age,
            "sex": self.sex,
            "use_llm": self.use_llm,
            "current_disorder_index": self.current_disorder_index,
            "current_stage": self.current_stage,
            "current_symptom_index": self.current_symptom_index,
            "scores": self.scores,
            "last_question": self.last_question,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, state: Dict[str, Any], disorders_map: Dict[str, Dict[str, list]]):
        """Restore session from state dict."""
        obj = cls(disorders_map, age=state.get("age", 30), sex=state.get("sex", "unknown"), use_llm=state.get("use_llm", True))
        obj.current_disorder_index = state.get("current_disorder_index", 0)
        obj.current_stage = state.get("current_stage", "core")
        obj.current_symptom_index = state.get("current_symptom_index", 0)
        obj.scores = state.get("scores", {d: [] for d in obj.disorder_names})
        obj.last_question = state.get("last_question", None)
        obj.completed = state.get("completed", False)
        return obj