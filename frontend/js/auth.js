document.addEventListener('DOMContentLoaded', (event) => {
    const otpInputs = document.querySelectorAll('.otp-input');
    
    otpInputs.forEach((input, index) => {
        input.addEventListener('input', () => {
            if (input.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && input.value.length === 0 && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });

    document.querySelector('.send-otp-btn').addEventListener('click', async function() {
        const cccd = document.querySelector('#cccd-input').value;
        console.log('Sending OTP to:', cccd); 
        const response = await fetch('/api/auth/send-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cccd: cccd })
        });
        const data = await response.json();
        console.log('Response:', data); 
        alert(data.message);
    });

    document.querySelector('form').addEventListener('submit', async function(event) {
        event.preventDefault();
        const cccd = document.querySelector('#cccd-input').value;
        const otp = Array.from(document.querySelectorAll('.otp-input')).map(input => input.value).join('');
        const response = await fetch('/api/auth/verify-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cccd: cccd, otp: otp })
        });
        const data = await response.json();
        if (data.message === 'OTP verified, redirect to voting page') {
            window.location.href = '/vote.html'; 
        } else {
            alert(data.message);
        }
    });

    document.querySelector('.signup-text a').addEventListener('click', async function(event) {
        event.preventDefault();
        const cccd = document.querySelector('#cccd-input').value;
        console.log('Resending OTP to:', cccd); 
        const response = await fetch('/api/auth/send-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cccd: cccd })
        });
        const data = await response.json();
        console.log('Response:', data); 
        alert(data.message);

        // Đếm ngược 60 giây
        const resendLink = document.querySelector('.signup-text a');
        let countdown = 60;
        resendLink.textContent = `Gửi lại (${countdown}s)`;
        resendLink.style.pointerEvents = 'none'; 

        const interval = setInterval(() => {
            countdown--;
            resendLink.textContent = `Gửi lại (${countdown}s)`;
            if (countdown === 0) {
                clearInterval(interval);
                resendLink.textContent = 'Gửi lại';
                resendLink.style.pointerEvents = 'auto';
            }
        }, 1000);
    });
});