from django.shortcuts import render, redirect
from .models import Teacher, Student
from authLogin.models import User
from django.contrib import messages
from education.models import ExamResults, Diploma

def profile_page(request):
    if not request.user.is_authenticated:
        return redirect('login-page')

    user = request.user
    context = {'user': user}

    if request.method == 'POST':
        if user.role == 'teacher':
            form_type = request.POST.get('form_type')
            if form_type == 'exam':
                return handle_create_exam(request)
            elif form_type == 'diploma':
                return handle_create_diploma(request)
            elif form_type == 'delete_exam':
                return handle_delete_exam(request)
            elif form_type == 'delete_diploma':
                return handle_delete_diploma(request)
        elif user.role == 'admin':
            from adminFunc.views import handle_admin_post
            return handle_admin_post(request)


    if user.role == 'student':
        student = user.student_profile
        context['student'] = student
        context['teacher'] = student.teacher
        context['exam_results'] = student.exam_results.all().order_by('-date')
        context['diplomas'] = student.diplomas.all()

    elif user.role == 'teacher':
        teacher = user.teacher_profile
        students = teacher.students.all()
        students_data = []
        for student in students:
            students_data.append({
                'student': student,
                'exams': student.exam_results.all().order_by('-date'),
                'diplomas': student.diplomas.all(),
            })
        context['teacher'] = teacher
        context['students_data'] = students_data
        context['student_choices'] = [(s.id, s.full_name) for s in students]

    elif user.role == 'admin':
        context['users_list'] = User.objects.all().order_by('-id')
        context['teachers'] = Teacher.objects.all()
        context['classes'] = range(1, 10)

    return render(request, 'profile.html', context)

# для учителя

def handle_create_exam(request):
    teacher = request.user.teacher_profile
    student_id = request.POST.get('student')
    heading = request.POST.get('heading')
    date = request.POST.get('date')
    mark = request.POST.get('mark')

    try:
        student = Student.objects.get(id=student_id)
        if student.teacher != teacher:
            messages.error(request, 'Это не ваш ученик')
            return redirect('profile-page')
        ExamResults.objects.create(student=student, teacher=teacher, heading=heading, date=date, mark=mark)
        messages.success(request, 'Оценка выставлена')
    except Student.DoesNotExist:
        messages.error(request, 'Ученик не найден')

    return redirect('profile-page')
def handle_delete_exam(request):
    exam_id = request.POST.get('exam_id')
    try:
        exam = ExamResults.objects.get(id=exam_id)
        if exam.student.teacher != request.user.teacher_profile:
            messages.error(request, 'Это не ваш ученик')
        else:
            exam.delete()
            messages.success(request, 'Оценка удалена')
    except ExamResults.DoesNotExist:
        messages.error(request, 'Оценка не найдена')
    return redirect('profile-page')


def handle_delete_diploma(request):
    diploma_id = request.POST.get('diploma_id')
    try:
        diploma = Diploma.objects.get(id=diploma_id)
        if diploma.student.teacher != request.user.teacher_profile:
            messages.error(request, 'Это не ваш ученик')
        else:
            diploma.delete()
            messages.success(request, 'Грамота удалена')
    except Diploma.DoesNotExist:
        messages.error(request, 'Грамота не найдена')
    return redirect('profile-page')


def handle_create_diploma(request):
    teacher = request.user.teacher_profile
    student_id = request.POST.get('student')
    file = request.FILES.get('file')

    try:
        student = Student.objects.get(id=student_id)
        if student.teacher != teacher:
            messages.error(request, 'Это не ваш ученик')
            return redirect('profile-page')
        Diploma.objects.create(student=student, file=file)
        messages.success(request, 'Грамота добавлена')
    except Student.DoesNotExist:
        messages.error(request, 'Ученик не найден')

    return redirect('profile-page')