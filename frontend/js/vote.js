document.addEventListener('DOMContentLoaded', async function () {
    // Xử lý sự kiện bỏ phiếu
    document.getElementById('candidate1').addEventListener('click', async function () {
        await vote(1);
    });

    document.getElementById('candidate2').addEventListener('click', async function () {
        await vote(2);
    });

    async function vote(candidate) {
        const response = await fetch('/api/vote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ candidate: candidate }),
        });

        const result = await response.json();
        if (result.message === 'Vote successful') {
            alert(result.message);
            window.location.href = '/results.html'; 
        } else {
            alert(result.message);
        }
    }

    // Đồng hồ đếm ngược
    const endDate = new Date('January 15, 2025 23:59:59').getTime();

    function updateCountdown() {
        const now = new Date().getTime();
        const distance = endDate - now;

        if (distance < 0) {
            clearInterval(countdownInterval);
            document.querySelector('.countdown-container').innerHTML =
                '<p>Voting period has ended</p>';
            return;
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.getElementById('days').textContent = days.toString().padStart(2, '0');
        document.getElementById('hours').textContent = hours.toString().padStart(2, '0');
        document.getElementById('minutes').textContent = minutes.toString().padStart(2, '0');
        document.getElementById('seconds').textContent = seconds.toString().padStart(2, '0');
    }

    const countdownInterval = setInterval(updateCountdown, 1000);
    updateCountdown(); 
});
