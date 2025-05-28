from django.db import models

class ExamLevel(models.Model):
    """Examples: HSC, Degree, Honours"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    """Group or Stream related to ExamLevel, e.g. Science, Humanities"""
    exam_level = models.ForeignKey(ExamLevel, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('exam_level', 'name')

    def __str__(self):
        return f"{self.name} ({self.exam_level.name})"


class Subject(models.Model):
    """Subjects related to a Group and ExamLevel"""
    exam_level = models.ForeignKey(ExamLevel, on_delete=models.CASCADE, related_name='subjects')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ('exam_level', 'group', 'name')

    def __str__(self):
        return self.name


class Exam(models.Model):
    """The exam itself for a specific level and group, with a name and date"""
    exam_level = models.ForeignKey(ExamLevel, on_delete=models.CASCADE, related_name='exams')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='exams')
    name = models.CharField(max_length=200)
    exam_date = models.DateField()

    subjects = models.ManyToManyField(Subject, blank=True, related_name='exams')

    def __str__(self):
        return f"{self.name} - {self.exam_level.name} - {self.group.name}"
