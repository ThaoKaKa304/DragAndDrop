from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import re
from collections import Counter

@api_view(['POST', 'OPTIONS'])
def word_count(request):
    if request.method == 'POST':
        # Kiểm tra xem file có phải là file .txt hay không
        if not request.FILES.get('file', None) or not request.FILES['file'].name.endswith('.txt'):
            return Response({'error': 'Invalid file format. Only .txt files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        # Đọc nội dung của file
        file = request.FILES['file']
        text = file.read().decode('utf-8')

        # Kiểm tra xem văn bản có chứa ký tự không hợp lệ hay không
        if re.search(r'[^a-zA-Z.,\s]', text):
            return Response({'error': 'Invalid characters in text. Only letters, commas, periods, and spaces are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        # Tính toán số từ khác nhau và 3 từ được lặp lại nhiều nhất
        word_counts = Counter(re.findall(r'\b\w+\b', text.lower()))
        num_unique_words = len(word_counts)
        most_common_words = word_counts.most_common(1)

        # Trả về kết quả
        return Response({'num_unique_words': num_unique_words, 'most_common_words': most_common_words})