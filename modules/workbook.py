from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from typing import List

from .const.settings import Business

def create_workbook(businesses: List[Business], output_file: str) -> None:
    """Create an Excel workbook with business data."""
    wb = Workbook()
    
    # Create main sheet
    ws_businesses = wb.active
    ws_businesses.title = 'Businesses'
    
    # Create reviews sheet
    ws_reviews = wb.create_sheet('Reviews')
    
    # Style definitions
    header_font = Font(bold=True, color='FFFFFF')
    header_fill = PatternFill(start_color='4F81BD', end_color='4F81BD', fill_type='solid')
    centered = Alignment(horizontal='center')
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Business sheet headers
    business_headers = [
        'Business Name',
        'Street Address',
        'Postal Code',
        'City',
        'Phone',
        'Website',
        'Average Rating',
        'Number of Reviews'
    ]
    
    # Review sheet headers
    review_headers = [
        'Business Name',
        'Review Text',
        'Rating',
        'Time Posted',
        'Positive Points',
        'Negative Points',
        'Services Used'
    ]
    
    # Setup business sheet
    for col, header in enumerate(business_headers, 1):
        cell = ws_businesses.cell(row=1, column=col)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = centered
        cell.border = border
    
    # Setup review sheet
    for col, header in enumerate(review_headers, 1):
        cell = ws_reviews.cell(row=1, column=col)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = centered
        cell.border = border
    
    # Fill business data
    for row, business in enumerate(businesses, 2):
        ws_businesses.cell(row=row, column=1).value = business.name
        ws_businesses.cell(row=row, column=2).value = business.street_address
        ws_businesses.cell(row=row, column=3).value = business.postal_code
        ws_businesses.cell(row=row, column=4).value = business.city
        ws_businesses.cell(row=row, column=5).value = business.phone
        ws_businesses.cell(row=row, column=6).value = business.website
        ws_businesses.cell(row=row, column=7).value = business.avg_rating
        ws_businesses.cell(row=row, column=8).value = business.num_ratings
    
    # Fill review data
    review_row = 2
    for business in businesses:
        for review in business.reviews:
            ws_reviews.cell(row=review_row, column=1).value = business.name
            ws_reviews.cell(row=review_row, column=2).value = review.text
            ws_reviews.cell(row=review_row, column=3).value = review.rating
            ws_reviews.cell(row=review_row, column=4).value = review.time_posted
            ws_reviews.cell(row=review_row, column=5).value = '\n'.join(review.positive_points) if review.positive_points else ''
            ws_reviews.cell(row=review_row, column=6).value = '\n'.join(review.negative_points) if review.negative_points else ''
            ws_reviews.cell(row=review_row, column=7).value = '\n'.join(review.services_used) if review.services_used else ''
            review_row += 1
    
    # Auto-adjust column widths
    for ws in [ws_businesses, ws_reviews]:
        for col in ws.columns:
            max_length = 0
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[get_column_letter(col[0].column)].width = adjusted_width
    
    # Save workbook
    wb.save(output_file)