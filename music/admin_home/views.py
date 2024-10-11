from django.shortcuts import render
from accounts.models import Customer

from checkout.models import Order, OrderItem, Payment
from datetime import datetime,timedelta
from django.db.models.functions import TruncDay,Cast
from django.db.models import DateField,Sum,Q,FloatField

# Create your views here.
def adminpanel(request):

     return render(request,'admin_panel.html')

def dashboard(request):
    
     sales = OrderItem.objects.all().count()
     users = Customer.objects.all().count()
     recent_sales = Order.objects.order_by('-id')[:5]
     # Graph setting
    # Getting the current date
     today = datetime.today()
     date_range = 8

    # Get the date 7 days ago
     four_days_ago = today - timedelta(days=date_range)

    #filter orders based on the date range
     payments = Payment.objects.filter(paid_date__gte=four_days_ago,paid_date__lte=today)

    # Getting the sales amount per day
     sales_by_day = payments.annotate(day=TruncDay('paid_date')).values('day').annotate(total_sales=Sum('cart_total')).order_by('day')
     context={
          'sales':sales,
          'users':users,
          "recent_sales":recent_sales,
          'sales_by_day': sales_by_day,

     }

     return render(request, 'dashboard.html',context)





