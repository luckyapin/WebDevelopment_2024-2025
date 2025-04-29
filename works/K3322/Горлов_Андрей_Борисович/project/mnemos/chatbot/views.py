from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from chatbot.pipeline.chatbot_interface import ChatSession
from django.views.decorators.http import require_POST
import markdown

def chat_home(request):
    # Инициализируем историю, если её нет в сессии
    chat_history = request.session.get('chat_history', [])

    # Для отладки: вывести историю в консоль сервера
    print("Текущая история чата:", chat_history)

    return render(request, 'chatbot/chat.html', {'chat_history': chat_history})


@csrf_protect
def send_message(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if user_message:
            try:
                # Получаем историю из сессии
                chat_history = request.session.get('chat_history', [])

                # Создаем сессию чата с историей пользователя
                chat_session = ChatSession(history=chat_history)
                response = chat_session.get_response(user_message)
                print(response)
                response = markdown.markdown(response)
                # Обновляем историю в сессии
                request.session['chat_history'] = chat_session.history
                request.session.modified = True
                print(response)

                return JsonResponse({
                    'success': True,
                    'bot_response': response
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
    return JsonResponse({'success': False})

@require_POST
def clear_history(request):
    if 'chat_history' in request.session:
        del request.session['chat_history']
        request.session.modified = True
    return redirect('chat_home')

