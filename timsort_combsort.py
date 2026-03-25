

class Student:
    def __init__(self, name, grade, section):
        self.name = name
        self.grade = grade
        self.section = section
    
    def __str__(self):
        return f"{self.name:12} Grade: {self.grade:3}  Section: {self.section}"


def print_students(students, title):
    print(f"\n{title}")
    print("-" * 45)
    for student in students:
        print(student)


def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i].grade <= right[j].grade:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def insertion_sort(students, left, right):
    for i in range(left + 1, right + 1):
        key_item = students[i]
        j = i - 1
        while j >= left and students[j].grade > key_item.grade:
            students[j + 1] = students[j]
            j -= 1
        students[j + 1] = key_item


def tim_sort(students):
    
    MIN_MERGE = 32
    n = len(students)
    students = students.copy()
    
    for start in range(0, n, MIN_MERGE):
        end = min(start + MIN_MERGE - 1, n - 1)
        insertion_sort(students, start, end)
    
    size = MIN_MERGE
    while size < n:
        for start in range(0, n, size * 2):
            mid = start + size - 1
            end = min(start + size * 2 - 1, n - 1)
            
            if mid < end:
                left = students[start:mid + 1]
                right = students[mid + 1:end + 1]
                merged = merge(left, right)
                students[start:end + 1] = merged
        
        size *= 2
    
    return students


def comb_sort(students):
    
    students = students.copy()
    n = len(students)
    gap = n
    shrink = 1.3
    sorted_flag = False
    
    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        
        i = 0
        while i + gap < n:
            if students[i].grade > students[i + gap].grade:
                students[i], students[i + gap] = students[i + gap], students[i]
                sorted_flag = False
            i += 1
    
    return students


def main():
    students = [
        Student("Alice", 85, "A"),
        Student("Bob", 92, "B"),
        Student("Charlie", 85, "A"),
        Student("Diana", 78, "C"),
        Student("Eve", 92, "B"),
        Student("Frank", 85, "C"),
        Student("Grace", 78, "A"),
        Student("Henry", 95, "B"),
        Student("Ivy", 78, "C"),
        Student("Jack", 92, "A"),
    ]
    
    print("=" * 45)
    print("  TIM SORT & COMB SORT DEMO")
    print("=" * 45)
    
    print_students(students, "📋 Original (by name):")
    
    print("\n" + "=" * 45)
    print("🟢 TIM SORT (STABLE)")
    print("=" * 45)
    students_tim = tim_sort(students)
    print_students(students_tim, "Sorted by grade:")
    print("\n✅ Grade 85: Alice → Charlie → Frank")
    print("✅ Grade 92: Bob → Eve → Jack")
    
    print("\n" + "=" * 45)
    print("🔴 COMB SORT (NON-STABLE)")
    print("=" * 45)
    students_comb = comb_sort(students)
    print_students(students_comb, "Sorted by grade:")
    print("\n⚠️  Grade 85: Order may change")
    print("⚠️  Grade 92: Order may change")


if __name__ == "__main__":
    main()
