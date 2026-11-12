class Quiz:
    def __init__(self, question, choices, answer, explanation):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.explanation = explanation

    def show_question(self, number):
        print(f"\n[{number}번 문제]")
        print(self.question)

        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0
        self.create_default_quizzes()

    def create_default_quizzes(self):
        self.quizzes.append(
            Quiz(
                "Python에서 문자열을 나타낼 때 사용하는 기호는?",
                ["[]", "{}", "'' 또는 \"\"", "()"],
                "3",
                "문자열은 작은따옴표 또는 큰따옴표로 감싸서 만듭니다."
            )
        )

        self.quizzes.append(
            Quiz(
                "Python에서 주석을 작성할 때 사용하는 기호는?",
                ["//", "#", "/* */", "--"],
                "2",
                "Python에서는 # 기호를 사용해 주석을 작성합니다."
            )
        )

        self.quizzes.append(
            Quiz(
                "리스트를 만들 때 사용하는 괄호는?",
                ["()", "{}", "[]", "<>"],
                "3",
                "리스트는 대괄호 []를 사용해 만듭니다."
            )
        )

        self.quizzes.append(
            Quiz(
                "반복문에 해당하는 것은?",
                ["if", "for", "def", "class"],
                "2",
                "for는 반복문을 만들 때 사용합니다."
            )
        )

        self.quizzes.append(
            Quiz(
                "함수를 만들 때 사용하는 키워드는?",
                ["function", "make", "def", "class"],
                "3",
                "Python에서는 def 키워드로 함수를 만듭니다."
            )
        )

    def show_menu(self):
        print("\n====== Python 퀴즈 게임 ======")
        print("1. 퀴즈 시작")
        print("2. 문제 개수 확인")
        print("3. 문제 추가")
        print("4. 종료")

    def start_quiz(self):
        self.score = 0

        print("\n퀴즈를 시작합니다!")

        for index, quiz in enumerate(self.quizzes, start=1):
            quiz.show_question(index)
            user_answer = input("정답 번호를 입력하세요: ")

            if quiz.check_answer(user_answer):
                print("정답입니다!")
                self.score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

            print(f"해설: {quiz.explanation}")

        print("\n====== 결과 ======")
        print(f"총 {len(self.quizzes)}문제 중 {self.score}문제를 맞혔습니다.")

    def show_quiz_count(self):
        print(f"\n현재 등록된 문제는 총 {len(self.quizzes)}개입니다.")

    def add_quiz(self):
        print("\n새 문제를 추가합니다.")

        question = input("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = input(f"{i}번 보기 입력: ")
            choices.append(choice)

        while True:
            answer = input("정답 번호를 입력하세요(1~4): ")

            if answer in ["1", "2", "3", "4"]:
                break

            print("1부터 4 사이의 숫자를 입력하세요.")

        explanation = input("해설을 입력하세요: ")

        new_quiz = Quiz(question, choices, answer, explanation)
        self.quizzes.append(new_quiz)

        print("문제가 추가되었습니다.")

    def run(self):
        while True:
            self.show_menu()
            menu = input("메뉴를 선택하세요: ")

            if menu == "1":
                self.start_quiz()
            elif menu == "2":
                self.show_quiz_count()
            elif menu == "3":
                self.add_quiz()
            elif menu == "4":
                print("퀴즈 게임을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다. 다시 선택하세요.")


game = QuizGame()
game.run()