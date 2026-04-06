import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class ExportService:
    @staticmethod
    def to_csv(queryset, filename, fields):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(fields)
        for obj in queryset:
            row = []
            for field in fields:
                val = getattr(obj, field, '')
                if callable(val): val = val()
                row.append(val)
            writer.writerow(row)
        return response

    @staticmethod
    def to_pdf(data, filename, title):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
        
        p = canvas.Canvas(response, pagesize=letter)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, title)
        
        p.setFont("Helvetica", 12)
        y = 720
        for line in data:
            p.drawString(100, y, str(line))
            y -= 20
            if y < 50:
                p.showPage()
                y = 750
        
        p.showPage()
        p.save()
        return response
