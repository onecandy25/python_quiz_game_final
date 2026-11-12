import json
import os

STATE_FILE = "state.json"  # 문제/최고점수를 저장할 파일


class Quiz:
    def __init__(self, question, choices, answer, explanation):
        self.question = question
        self.choices = choices
        self.answer = answer            # 정답은 숫자(int)로 관리
        self.explanation = explanation

    def show_question(self, number):
        print(f"\n[{number}번 문제]")
        print(self.question)
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        # 저장용: 객체 → 딕셔너리
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "explanation": self.explanation,
        }

    @staticmethod
    def from_dict(data):
        # 불러오기용: 딕셔너리 → 객체
        return Quiz(
            data["question"],
            data["choices"],
            data["answer"],
            data["explanation"],
        )


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0
        self.best_score = 0
        self.load_state()  # 시작할 때 저장된 데이터 불러오기

    # ---------- 기본 문제 ----------
    def create_default_quizzes(self):
        self.quizzes = [
            Quiz(
                "Python에서 문자열을 나타낼 때 사용하는 기호는?",
                ["[]", "{}", "'' 또는 \"\"", "()"],
                3,
                "문자열은 작은따옴표 또는 큰따옴표로 감싸서 만듭니다."
            ),
            Quiz(
                "Python에서 주석을 작성할 때 사용하는 기호는?",
                ["//", "#", "/* */", "--"],
                2,
                "Python에서는 # 기호를 사용해 주석을 작성합니다."
            ),
            Quiz(
                "리스트를 만들 때 사용하는 괄호는?",
                ["()", "{}", "[]", "<>"],
                3,
                "리스트는 대괄호 []를 사용해 만듭니다."
            ),
            Quiz(
                "반복문에 해당하는 것은?",
                ["if", "for", "def", "class"],
                2,
                "for는 반복문을 만들 때 사용합니다."
            ),
            Quiz(
                "함수를 만들 때 사용하는 키워드는?",
                ["function", "make", "def", "class"],
                3,
                "Python에서는 def 키워드로 함수를 만듭니다."
            ),
        ]

    # ---------- 저장 / 불러오기 ----------
    def save_state(self):
        data = {
            "best_score": self.best_score,
            "quizzes": [q.to_dict() for q in self.quizzes],
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"저장 중 오류가 발생했습니다: {e}")

    def load_state(self):
        # 파일이 없으면 기본 문제로 시작
        if not os.path.exists(STATE_FILE):
            self.create_default_quizzes()
            return
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.best_score = data.get("best_score", 0)
            self.quizzes = [Quiz.from_dict(d) for d in data.get("quizzes", [])]
            # 저장 파일은 있는데 문제가 비어 있으면 기본 문제로 보충
            if not self.quizzes:
                self.create_default_quizzes()
        except (OSError, json.JSONDecodeError, KeyError):
            print("저장 파일을 읽지 못해 기본 문제로 시작합니다.")
            self.create_default_quizzes()

    # ---------- 입력 도우미 ----------
    def input_safe(self, prompt):
        # 입력 중단(Ctrl+C, Ctrl+D) 시 None 반환
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n입력이 중단되었습니다.")
            return None

    # ---------- 메뉴 ----------
    def show_menu(self):
        print("\n====== Python 퀴즈 게임 ======")
        print(f"(최고 점수: {self.best_score}점)")
        print("1. 퀴즈 시작")
        print("2. 문제 개수 확인")
        print("3. 문제 추가")
        print("4. 종료")

    # ---------- 퀴즈 진행 ----------
    def start_quiz(self):
        if not self.quizzes:
            print("\n등록된 문제가 없습니다.")
            return

        self.score = 0
        print("\n퀴즈를 시작합니다!")

        for index, quiz in enumerate(self.quizzes, start=1):
            quiz.show_question(index)

            user_answer = self.input_safe("정답 번호를 입력하세요: ")
            if user_answer is None:
                print("퀴즈를 중단합니다.")
                return

            if not user_answer.isdigit():
                print("숫자를 입력해야 합니다. 오답 처리합니다.")
                print(f"정답은 {quiz.answer}번입니다. 해설: {quiz.explanation}")
                continue

            if quiz.check_answer(int(user_answer)):
                print("정답입니다!")
                self.score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

            print(f"해설: {quiz.explanation}")

        print("\n====== 결과 ======")
        print(f"총 {len(self.quizzes)}문제 중 {self.score}문제를 맞혔습니다.")

        if self.score > self.best_score:
            self.best_score = self.score
            print(f"🎉 신기록 달성! 최고 점수: {self.best_score}점")
            self.save_state()  # 최고 점수 갱신 시 저장

            def show_quiz_count(self):
            print(f"\n현재 등록된 문제는 총 {len(self.quizzes)}개입니다.")

    # ---------- 문제 추가 ----------
    def add_quiz(self):
        print("\n새 문제를 추가합니다.")

        question = self.input_safe("문제를 입력하세요: ")
        if not question:
            print("문제를 입력하지 않아 취소되었습니다.")
            return

        choices = []
        for i in range(1, 5):
            choice = self.input_safe(f"{i}번 보기 입력: ")
            if not choice:
                print("보기를 입력하지 않아 취소되었습니다.")
                return
            choices.append(choice)

        while True:
            answer = self.input_safe("정답 번호를 입력하세요(1~4): ")
            if answer is None:
                print("문제 추가를 취소합니다.")
                return
            if answer in ["1", "2", "3", "4"]:
                answer = int(answer)
                break
            print("1부터 4 사이의 숫자를 입력하세요.")

        explanation = self.input_safe("해설을 입력하세요: ")
        if explanation is None:
            explanation = ""

        self.quizzes.append(Quiz(question, choices, answer, explanation))
        self.save_state()  # 추가 후 바로 저장
        print("문제가 추가되었습니다.")

    # ---------- 실행 ----------
    def run(self):
        while True:
            self.show_menu()
            menu = self.input_safe("메뉴를 선택하세요: ")

            if menu is None:          # 입력 중단 시 종료
                menu = "4"

            if menu == "1":
                self.start_quiz()
            elif menu == "2":
                self.show_quiz_count()
            elif menu == "3":
                self.add_quiz()
            elif menu == "4":
                self.save_state()     # 종료 전 저장
                print("퀴즈 게임을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다. 다시 선택하세요.")


game = QuizGame()
game.run()