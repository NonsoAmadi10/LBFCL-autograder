import os
import json
from tests.week1_test import grade_week1
from tests.utils import detect_plagiarism, read_file_content

def grade_student(student_folder):
    results = {}
    week1_folder = os.path.join(student_folder, 'week1')
    if not os.path.exists(week1_folder):
        results['week1'] = {
            'score': 0,
            'feedback': ['Week 1 folder not found']
        }
        return results

    week_content = {}
    for file in os.listdir(week1_folder):
        file_path = os.path.join(week1_folder, file)
        week_content[file] = read_file_content(file_path)

    score, feedback = grade_week1(week_content)
    results['week1'] = {
        'score': score,
        'feedback': feedback
    }

    return results

def grade_all_submissions(submissions_dir):
    all_results = {}
    all_submissions = {}
    for student in os.listdir(submissions_dir):
        student_folder = os.path.join(submissions_dir, student)
        if os.path.isdir(student_folder):
            all_results[student] = grade_student(student_folder)
            all_submissions[student] = {}
            week1_folder = os.path.join(student_folder, 'week1')
            if os.path.exists(week1_folder):
                all_submissions[student]['week1'] = {
                    file: read_file_content(os.path.join(week1_folder, file))
                    for file in os.listdir(week1_folder)
                }

    # Detect plagiarism
    plagiarism_results = detect_plagiarism(all_submissions)

    # Add plagiarism results to the grading results
    for student, plagiarism_info in plagiarism_results.items():
        all_results[student]['plagiarism_warning'] = [
            f"High similarity ({similarity:.2f}) with {other_student}"
            for other_student, similarity in plagiarism_info
        ]

    return all_results

if __name__ == "__main__":
    submissions_dir = "submissions"
    results = grade_all_submissions(submissions_dir)
    
    with open("grades.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("Grading completed. Results written to grades.json")
