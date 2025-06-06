from django.db import models

# Create your models here.
from datetime import datetime

from django.db import models

class Candidate(models.Model):
    user_id = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    keywords = models.TextField()
    awards = models.TextField()
    education = models.TextField()
    graduation_date = models.CharField(max_length=255)
    job_title = models.TextField()
    previous_organization = models.TextField()
    certifications = models.TextField()


    def calculate_age(self):
        if self.graduation_date:
            try:
                graduation_year = int(self.graduation_date.split()[-1])
                current_year = datetime.now().year
                age = current_year - graduation_year
                return age+21
            except ValueError:
                pass
        return None

    def calculate_experience(self):
        if self.job_title:
            job_titles = eval(self.job_title)
            return len(job_titles)
        return None

    def age_and_experience_range(self):
        age = self.calculate_age()
        experience = self.calculate_experience()

        if age and experience:
            return f"Age: {age} years | Experience: {experience} years"
        elif age:
            return f"Age: {age} years"
        elif experience:
            return f"Experience: {experience} years"
        else:
            return "Age and experience information unavailable"







