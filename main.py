"""
PS 65 - Student Fee Management System
Language: Python 3
Concepts: Dictionaries, Functions, Conditions, File Handling

Records are stored in fees.txt as:  Roll,Name,Course,Paid
Status is calculated, never stored:
    Paid    -> due == 0
    Partial -> 0 < paid < total
    Unpaid  -> paid == 0
"""

import os

FILE_NAME = "fees.txt"

# Course-fee table (dictionary)
COURSE_FEES = {
    "BCA": 45000,
    "BTECH": 60000,
    "MBA": 80000,
}

# Display names for courses (so BTech prints nicely)
COURSE_LABELS = {"BCA": "BCA", "BTECH": "BTech", "MBA": "MBA"}


# ---------------------------------------------------------------- helpers
def calc_due(student):
    """Return the amount still to be paid."""
    return COURSE_FEES[student["course"]] - student["paid"]


def calc_status(student):
    """Return Paid / Partial / Unpaid based on due and paid."""
    total = COURSE_FEES[student["course"]]
    if student["paid"] == 0:
        return "Unpaid"
    if student["paid"] >= total:
        return "Paid"
    return "Partial"


def find_student(students, roll):
    """Search a student by roll number. Returns the dict or None."""
    for s in students:
        if s["roll"] == roll:
            return s
    return None


def read_positive_int(prompt):
    """Read an integer from the user. Returns None if input is not a number."""
    text = input(prompt).strip()
    try:
        return int(text)
    except ValueError:
        return None


def show_line(student):
    """One-line summary of a student."""
    total = COURSE_FEES[student["course"]]
    return (f"{student['roll']} | {student['name']} | "
            f"{COURSE_LABELS[student['course']]} | Total Fee: {total} | "
            f"Paid: {student['paid']} | Due: {calc_due(student)} | "
            f"Status: {calc_status(student)}")


# ---------------------------------------------------------- file handling
def load_records():
    """Load students from fees.txt into a list of dictionaries."""
    students = []
    if not os.path.exists(FILE_NAME):
        return students
    with open(FILE_NAME, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) < 4:
                continue  # skip damaged line
            roll, name, course, paid = parts[0], parts[1], parts[2].upper(), parts[3]
            if course not in COURSE_FEES or not paid.isdigit():
                continue
            students.append({
                "roll": int(roll),
                "name": name,
                "course": course,
                "paid": int(paid),
            })
    return students


def save_records(students):
    """Write all students back to fees.txt."""
    with open(FILE_NAME, "w") as f:
        for s in students:
            f.write(f"{s['roll']},{s['name']},{s['course']},{s['paid']}\n")


# --------------------------------------------------------------- features
def add_student(students):
    roll = read_positive_int("Roll: ")
    if roll is None or roll <= 0:
        print("Invalid roll number.")
        return
    if find_student(students, roll) is not None:
        print("Roll number already exists.")
        return

    name = input("Name: ").strip()
    if name == "" or "," in name:
        print("Invalid name.")
        return

    course = input("Course (BCA/BTech/MBA): ").strip().upper()
    if course not in COURSE_FEES:
        print("Invalid course. Choose BCA, BTech or MBA.")
        return

    student = {"roll": roll, "name": name, "course": course, "paid": 0}
    students.append(student)
    save_records(students)
    print("Student added:", show_line(student).replace(" | Status", " | Status", 1))


def pay_fee(students):
    roll = read_positive_int("Roll: ")
    if roll is None:
        print("Invalid roll number.")
        return
    student = find_student(students, roll)
    if student is None:
        print("Student not found.")
        return

    amount = read_positive_int("Amount: ")
    due = calc_due(student)

    if amount is None:
        print("Invalid amount.")
    elif amount <= 0:
        print("Amount must be greater than zero. Payment rejected.")
    elif amount > due:
        print(f"Amount exceeds due ({due}). Payment rejected.")
    else:
        student["paid"] += amount
        save_records(students)
        print(f"Payment received. Paid: {student['paid']} | "
              f"Due: {calc_due(student)} | Status: {calc_status(student)}")


def search_student(students):
    roll = read_positive_int("Roll: ")
    if roll is None:
        print("Invalid roll number.")
        return
    student = find_student(students, roll)
    if student is None:
        print("Student not found.")
    else:
        print(show_line(student))


def list_pending(students):
    found = False
    for s in students:
        due = calc_due(s)
        if due > 0:
            print(f"{s['roll']} | {s['name']} | Due: {due}")
            found = True
    if not found:
        print("No pending dues.")


# ------------------------------------------------------------------- main
def main():
    students = load_records()
    while True:
        print("\n===== Student Fee Management System =====")
        print("1. Add student")
        print("2. Pay fee")
        print("3. Search student")
        print("4. Pending dues")
        print("5. Exit")
        choice = input("Choose option: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            pay_fee(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            list_pending(students)
        elif choice == "5":
            save_records(students)
            print("Goodbye!")
            break
        else:
            print("Invalid option. Enter 1-5.")


if __name__ == "__main__":
    main()
    