from faker import Faker
import random, csv, os
from datetime import date, timedelta

fake = Faker()
random.seed(7)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def write_csv(rel_path, header, rows):
    path = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

def iso(d): return d.isoformat()

def gen_retail(n_customers=500, n_products=80, n_orders=2000):
    # customers
    customers=[]
    for cid in range(1, n_customers+1):
        name = fake.name() if random.random() > 0.03 else "   "
        email = fake.email() if random.random() > 0.06 else ""
        customers.append([cid, name, email, fake.city(), fake.state_abbr(), iso(fake.date_between(start_date="-2y", end_date="today"))])
    # products
    categories = ["Accessories","Office","Audio","Storage","Networking"]
    products=[]
    for pid in range(1001, 1001+n_products):
        price = round(random.uniform(8, 220), 2)
        if random.random() < 0.04: price = ""  # missing
        products.append([pid, fake.word().capitalize()+" "+random.choice(["Cable","Stand","Mouse","Hub","Adapter","Drive","Router"]), random.choice(categories), price, 1])
    # orders + items
    statuses = ["Shipped","Shipped","Shipped","Returned","Canceled"]
    channels = ["Web","Mobile","Partner"]
    orders=[]
    order_items=[]
    order_item_id=1
    start = date.today() - timedelta(days=365)
    for oid in range(50001, 50001+n_orders):
        cid = random.randint(1, n_customers)
        od = start + timedelta(days=random.randint(0, 364))
        status = random.choice(statuses)
        channel = random.choice(channels)
        ship = round(max(0, random.gauss(6, 2)), 2)
        if random.random() < 0.03: ship = ""  # missing
        orders.append([oid, cid, iso(od), status, channel, ship])
        # 1-5 items
        for _ in range(random.randint(1,5)):
            pid = random.choice(products)[0]
            qty = random.randint(1,4)
            unit_price = "" if random.random() < 0.03 else round(random.uniform(8, 220), 2)
            discount = "" if random.random() < 0.20 else round(random.uniform(0, 10), 2)
            order_items.append([order_item_id, oid, pid, qty, unit_price, discount])
            order_item_id += 1
    write_csv("01_retail_sales_analytics/data/raw/customers.csv",
              ["customer_id","full_name","email","city","state","created_at"], customers)
    write_csv("01_retail_sales_analytics/data/raw/products.csv",
              ["product_id","product_name","category","unit_price","active"], products)
    write_csv("01_retail_sales_analytics/data/raw/orders.csv",
              ["order_id","customer_id","order_date","status","channel","shipping_cost"], orders)
    write_csv("01_retail_sales_analytics/data/raw/order_items.csv",
              ["order_item_id","order_id","product_id","quantity","unit_price","discount"], order_items)

def gen_hr(n=400):
    depts=["Sales","Engineering","Support","Finance","Marketing"]
    roles={"Sales":["AE","SDR"],"Engineering":["SWE","SRE","Data"],"Support":["T1","T2"],"Finance":["Analyst"],"Marketing":["Coordinator","Manager"]}
    locations=["Remote","NYC","ATL","CLT","CHI"]
    rows=[]
    for eid in range(1,n+1):
        dept=random.choice(depts)
        role=random.choice(roles[dept])
        hire=fake.date_between(start_date="-6y", end_date="-30d")
        terminated = random.random() < 0.22
        term = fake.date_between(start_date=hire, end_date="today") if terminated else ""
        salary = int(random.uniform(45000, 160000))
        if random.random() < 0.03: salary = ""  # missing
        rating = random.choice([1,2,3,4,5])
        # dirty categories
        dept_dirty = dept if random.random() > 0.10 else dept.lower()+" "
        rows.append([eid, fake.name(), dept_dirty, role, random.choice(locations), hire.isoformat(), term if term=="" else term.isoformat(), salary, rating])
    write_csv("02_hr_attrition/data/raw/employee_roster.csv",
              ["employee_id","full_name","department","role","location","hire_date","termination_date","salary","performance_rating"], rows)

def gen_healthcare(n=2500):
    clinics=["North","South","East","West"]
    providers=[fake.name()[0]+". "+fake.last_name() for _ in range(12)]
    insurance=["Commercial","Medicaid","Medicare","SelfPay"]
    statuses=["Completed","Completed","Completed","NoShow","Canceled"]
    rows=[]
    base = date.today() - timedelta(days=365)
    for aid in range(1,n+1):
        patient_id = random.randint(2000, 6000)
        clinic=random.choice(clinics)
        provider=random.choice(providers)
        booked = base + timedelta(days=random.randint(0, 360))
        appt = booked + timedelta(days=random.randint(0, 40))
        status=random.choice(statuses)
        ins=random.choice(insurance)
        if random.random()<0.02: provider="  "  # blank
        rows.append([aid, patient_id, clinic, provider, iso(booked), iso(appt), status, ins])
    write_csv("03_healthcare_appointments/data/raw/appointments.csv",
              ["appointment_id","patient_id","clinic","provider","booked_at","appointment_at","status","insurance_type"], rows)

def gen_saas(n_accounts=600, n_subs=800):
    industries=["Healthcare","Retail","Manufacturing","Tech","Education"]
    plans=[("Basic",19),("Pro",49),("Business",99)]
    rows=[]
    for sid in range(1, n_subs+1):
        account = random.randint(9000, 9000+n_accounts-1)
        plan, price = random.choice(plans)
        start = fake.date_between(start_date="-24mo", end_date="-10d")
        churn = random.random() < 0.28
        end = fake.date_between(start_date=start, end_date="today") if churn else ""
        seats = random.choice([1,2,3,5,10,15,25,50])
        if random.random()<0.03: seats=""  # missing
        rows.append([sid, account, plan, start.isoformat(), "" if end=="" else end.isoformat(), price, random.choice(industries), seats])
    write_csv("04_saas_subscriptions/data/raw/subscriptions.csv",
              ["subscription_id","account_id","plan","start_date","end_date","monthly_price","industry","seats"], rows)

if __name__ == "__main__":
    gen_retail()
    gen_hr()
    gen_healthcare()
    gen_saas()
    print("Generated all CSVs into each project's data/raw/ folder.")
