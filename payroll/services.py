from decimal import Decimal

def calculate_salary(basic, hra_rate=Decimal("0.40"), allowances=0, bonus=0, pf_rate=Decimal("0.12"), tax=0, other_deductions=0, leave_days=0, working_days=26):
    basic = Decimal(str(basic)); allowances=Decimal(str(allowances or 0)); bonus=Decimal(str(bonus or 0)); tax=Decimal(str(tax or 0)); other=Decimal(str(other_deductions or 0))
    hra = basic * hra_rate
    gross = basic + hra + allowances + bonus
    pf = basic * pf_rate
    per_day = gross / Decimal(working_days) if working_days else Decimal("0")
    leave_deduction = per_day * max(0, int(leave_days))
    total = pf + tax + other + leave_deduction
    return {"basic":basic,"hra":hra,"allowances":allowances,"bonus":bonus,"gross":gross,"pf":pf,"tax":tax,"other_deductions":other,"leave_deduction":leave_deduction,"total_deductions":total,"net":max(Decimal("0"),gross-total)}
