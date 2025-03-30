document.addEventListener('DOMContentLoaded', async function () {
    // Hàm lấy kết quả bỏ phiếu từ API
    async function getResults() {
        try {
            const response = await fetch('/api/vote/candidate-votes');
            
            if (!response.ok) {
                throw new Error(`Failed to fetch data: ${response.status}`);
            }

            const data = await response.json();

            
            const candidate1Element = document.getElementById('candidate1-votes');
            const candidate2Element = document.getElementById('candidate2-votes');

            if (candidate1Element && candidate2Element) {
                candidate1Element.textContent = data.candidate1_votes;
                candidate2Element.textContent = data.candidate2_votes;

                
                updateChart(data.candidate1_votes, data.candidate2_votes);
            } else {
                console.error('DOM elements for vote results not found.');
            }

        } catch (error) {
            console.error('Error fetching voting results:', error.message);
        }
    }

    
    async function fetchResults() {
        try {
            const results = await contract.methods.getVotes().call();
            displayResults(results);
        } catch (error) {
            console.error('Error fetching voting results from smart contract:', error.message);
        }
    }

    // Hàm cập nhật biểu đồ
    function updateChart(candidate1Votes, candidate2Votes) {
        if (resultsChart) {
            resultsChart.data.datasets[0].data = [candidate1Votes, candidate2Votes];
            resultsChart.update();
        }
    }

    // Tạo biểu đồ tròn
    const ctx = document.getElementById('resultsChart').getContext('2d');
    const resultsChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Đỗ Nam Trâm', 'Dôn Bí Đèn'],
            datasets: [{
                label: 'Votes',
                data: [0, 0],
                backgroundColor: ['#007bff', '#ff69b4'],
                borderColor: ['#0056b3', '#ff1493'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            return `${label}: ${value} votes`;
                        }
                    }
                },
                datalabels: {
                    formatter: (value, context) => {
                        const totalVotes = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                        const percentage = totalVotes ? (value / totalVotes * 100).toFixed(2) : 0;
                        return `${percentage}%`;
                    },
                    color: '#fff',
                    backgroundColor: '#000',
                    borderRadius: 3,
                    padding: 6
                }
            }
        },
        plugins: [ChartDataLabels]
    });

    // Lấy kết quả bỏ phiếu khi tải trang
    await getResults();

    // Cập nhật kết quả bỏ phiếu mỗi 5 giây
    setInterval(getResults, 5000);
});