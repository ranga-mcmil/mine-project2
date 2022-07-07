from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Claim, Proof, Payment
from accounts.models import User
from .forms import ProofForm, ClaimForm, PaymentForm


@login_required
def dashboard(request):
    forfeited_claims = Claim.forfeited.all()
    if request.user.is_mine:
        active_claims = Claim.active.filter(applicant=request.user)
        pending_claims = Claim.pending_approval.filter(applicant=request.user)
        user = get_object_or_404(User, id=request.user.id)
        context = {
            'active_claims': active_claims,
            'pending_claims': pending_claims,
            'user': user,
            'forfeited_claims': forfeited_claims
        }
        return render(request, 'mine_mgt/miner/dashboard.html', context)
    else:
        active_claims = Claim.active.filter()
        pending_claims = Claim.pending_approval.filter()
        context = {
            'active_claims': active_claims,
            'pending_claims': pending_claims,
            'forfeited_claims': forfeited_claims
        }
        return render(request, 'mine_mgt/admin/dashboard.html', context)


@login_required
def payments(request):
    if request.user.is_mine:
        if request.method == 'POST':
            form = ProofForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                new_proof = form.save(commit=False)
                new_proof.uploaded_by = get_object_or_404(User, id=request.user.id)
                new_proof.save()
                return redirect('mine_mgt:payments')
        else:
            form = ProofForm()
        payments = Payment.objects.filter(user=request.user)
        proofs = Proof.objects.filter(uploaded_by=request.user)
        context = {
            'payments': payments,
            'proofs': proofs,
            'form': form
        }
        return render(request, 'mine_mgt/miner/payments.html', context)
    else:
        payments = Payment.objects.filter()
        proofs = Proof.objects.exclude(is_processeed=True)
        context = {
            'payments': payments,
            'proofs': proofs,
        }
        return render(request, 'mine_mgt/admin/payments.html', context)



@login_required
def claim_detail(request, id):
    if request.user.is_administrator:
        claim = get_object_or_404(Claim, id=id)
        proofs = Proof.objects.filter(uploaded_by=request.user)
        payments = Payment.objects.filter(user=request.user)
        context = {
            'claim': claim,
            'proofs': proofs,
            'payments': payments
        }
        return render(request, 'mine_mgt/admin/claim_detail.html', context)
    else:
        return redirect('mine_mgt:dashboard')


@login_required
def claim_application(request, id):
    if request.user.is_administrator:
        claim = get_object_or_404(Claim, id=id)
        pending_claims = Claim.pending_approval.exclude(id=id)
        context = {
            'claim': claim,
            'pending_claims': pending_claims
        }
        return render(request, 'mine_mgt/admin/claim_application.html', context)
    else:
        return redirect('mine_mgt:dashboard')

@login_required
def accept(request, id):
    claim = get_object_or_404(Claim, id=id)
    claim.status = 'active'
    claim.save()
    return redirect('mine_mgt:dashboard')

@login_required
def apply(request):
    claims = Claim.forfeited.all()
    if request.method == 'POST':
        form = ClaimForm(data=request.POST)
        if form.is_valid():
            new_claim = form.save(commit=False)
            new_claim.applicant = get_object_or_404(User, id=request.user.id)
            new_claim.save()
            return redirect('mine_mgt:dashboard')
    else:
        form = ClaimForm()

    context = {
        'claims': claims,
        'form': form
    }
    return render(request, 'mine_mgt/miner/apply.html', context)


@login_required
def apply_forfeited(request, id):
    claim = Claim.forfeited.get(id=id)
    claim.applicant = get_object_or_404(User, id=request.user.id)
    claim.status = 'pending_approval'
    claim.save()
    return redirect('mine_mgt:dashboard')


@login_required
def forfeited(request, id):
    claim = Claim.forfeited.get(id=id)
    claims = Claim.forfeited.exclude(id=id)
    context = {
        'claim': claim,
        'claims': claims
    }

    return render(request, 'mine_mgt/miner/forfeited.html', context)



@login_required
def add_payment(request, id):
    proof = get_object_or_404(Proof, id=id)
    user = proof.uploaded_by
    if request.method == 'POST':
        form = PaymentForm(data=request.POST)
        if form.is_valid():
            new_payment = form.save(commit=False)
            new_payment.user = get_object_or_404(User, id=proof.uploaded_by.id)
            new_payment.proof = proof
            new_payment.is_processeed = True
            print('434343434343434333334343', new_payment)
            new_payment.save()
            proof.is_processeed = True
            proof.save()
            return redirect('mine_mgt:dashboard')
    else:
        form = PaymentForm()

    context = {
        'proof': proof,
        'form': form,
        'user': user
    }

    return render(request, 'mine_mgt/admin/add_payment.html', context)


@login_required
def claims_on_offer(request):
    claims = Claim.forfeited.all()

    context = {
        'claims': claims
    }

    return render(request, 'mine_mgt/miner/claims_on_offer.html', context)