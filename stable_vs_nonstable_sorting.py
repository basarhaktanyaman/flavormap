

class Student:
    def __init__(self, name, grade, section):
        self.name = name
        self.grade = grade
        self.section = section
    
    def __repr__(self):
        return f"Student('{self.name}', grade={self.grade}, section='{self.section}')"
    
    def __str__(self):
        return f"{self.name:15} Grade: {self.grade:3}  Section: {self.section}"


def print_students(students, title):
    
    print(f"\n{title}")
    print("-" * 50)
    for student in students:
        print(student)


def merge_sort_stable(students):
    
    if len(students) <= 1:
        return students
    
    mid = len(students) // 2
    left = merge_sort_stable(students[:mid])
    right = merge_sort_stable(students[mid:])
    
    return merge(left, right)


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


def quicksort_nonstable(students, low=0, high=None):
    
    if high is None:
        high = len(students) - 1
    
    if low < high:
        pi = partition(students, low, high)
        quicksort_nonstable(students, low, pi - 1)
        quicksort_nonstable(students, pi + 1, high)
    
    return students


def partition(students, low, high):
    
    pivot = students[high].grade
    i = low - 1
    
    for j in range(low, high):
        if students[j].grade <= pivot:
            i += 1
            students[i], students[j] = students[j], students[i]
    
    students[i + 1], students[high] = students[high], students[i + 1]
    return i + 1


def insertion_sort(students, left, right):
    for i in range(left + 1, right + 1):
        key_item = students[i]
        j = i - 1
        while j >= left and students[j].grade > key_item.grade:
            students[j + 1] = students[j]
            j -= 1
        students[j + 1] = key_item


def tim_sort_stable(students):
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


def comb_sort_nonstable(students):
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
    
    students_original = [
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
    
    print("=" * 50)
    print("STABLE vs NON-STABLE SORTING DEMONSTRATION")
    print("=" * 50)
    
    print_students(students_original, "📋 ORIGINAL LIST (Sorted by name alphabetically):")
    
    
    print("\n" + "=" * 50)
    print("🟢 STABLE SORTING (Merge Sort)")
    print("=" * 50)
    students_stable = students_original.copy()
    students_stable = merge_sort_stable(students_stable)
    print_students(students_stable, "✅ After sorting by grade (STABLE):")
    
    print("\n📊 Notice: Students with same grade maintain their original name order!")
    print("   Grade 78: Diana → Grace → Ivy (alphabetical order preserved)")
    print("   Grade 85: Alice → Charlie → Frank (alphabetical order preserved)")
    print("   Grade 92: Bob → Eve → Jack (alphabetical order preserved)")
    
    
    print("\n" + "=" * 50)
    print("🔴 NON-STABLE SORTING (Quick Sort)")
    print("=" * 50)
    students_nonstable = students_original.copy()
    students_nonstable = quicksort_nonstable(students_nonstable)
    print_students(students_nonstable, "⚠️  After sorting by grade (NON-STABLE):")
    
    print("\n📊 Notice: Students with same grade may NOT maintain their original order!")
    print("   The relative ordering among equal grades can be different from the original.")
    
    
    print("\n" + "=" * 50)
    print("🟢 TIM SORT (STABLE)")
    print("=" * 50)
    students_timsort = students_original.copy()
    students_timsort = tim_sort_stable(students_timsort)
    print_students(students_timsort, "✅ After sorting by grade (TIM SORT - STABLE):")
    
    print("\n📊 Tim Sort is a hybrid algorithm (Insertion Sort + Merge Sort)")
    print("   It's used by Python and Java as their default sorting algorithm!")
    print("   Grade 78: Diana → Grace → Ivy (alphabetical order preserved)")
    print("   Grade 85: Alice → Charlie → Frank (alphabetical order preserved)")
    print("   Grade 92: Bob → Eve → Jack (alphabetical order preserved)")
    
    
    print("\n" + "=" * 50)
    print("🔴 COMB SORT (NON-STABLE)")
    print("=" * 50)
    students_combsort = students_original.copy()
    students_combsort = comb_sort_nonstable(students_combsort)
    print_students(students_combsort, "⚠️  After sorting by grade (COMB SORT - NON-STABLE):")
    
    print("\n📊 Comb Sort is an improved version of Bubble Sort")
    print("   It uses a gap larger than 1 initially and shrinks it")
    print("   Like Quick Sort, it does NOT maintain relative order of equal elements!")
    
    
    print("\n" + "=" * 50)
    print("🟢 PYTHON'S BUILT-IN SORT (Timsort - STABLE)")
    print("=" * 50)
    students_python = students_original.copy()
    students_python.sort(key=lambda s: s.grade)
    print_students(students_python, "✅ After sorting by grade using .sort():")
    
    print("\n" + "=" * 50)
    print("💡 KEY TAKEAWAYS")
    print("=" * 50)
    print("   ✅ Stable sorts preserve the original order for equal elements.")
    print("   ✅ This is crucial when you need to maintain multiple sort criteria!")
    print("\n🎓 STABLE algorithms: Merge Sort, Tim Sort, Counting Sort, Insertion Sort")
    print("⚡ NON-STABLE algorithms: Quick Sort, Heap Sort, Selection Sort, Comb Sort")


if __name__ == "__main__":
    main()

