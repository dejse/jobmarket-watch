from django.db import models


class JobData(models.Model):
    """Model representing job market data for Austrian cities"""
    date = models.DateField(db_index=True)
    location = models.CharField(max_length=100, db_index=True)
    job_count = models.IntegerField()

    class Meta:
        ordering = ['-date', 'location']
        indexes = [
            models.Index(fields=['date', 'location']),
        ]
        unique_together = ['date', 'location']
        verbose_name = 'Job Data'
        verbose_name_plural = 'Job Data'

    def __str__(self):
        return f"{self.location} - {self.date}: {self.job_count} jobs"
