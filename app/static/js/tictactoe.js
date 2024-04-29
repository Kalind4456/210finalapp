
document.addEventListener('DOMContentLoaded', function() {
    const cells = document.querySelectorAll('.cell');
    const status = document.getElementById('game-status');

    // Initialize game state
    let currentPlayer = 'X';
    let gameEnded = false;
    const board = ['', '', '', '', '', '', '', '', ''];

    // Add click event listener to each cell
    cells.forEach(cell => {
        cell.addEventListener('click', () => {
            if (!gameEnded && cell.textContent === '') {
                const index = cell.getAttribute('data-index');
                cell.textContent = currentPlayer;
                board[index] = currentPlayer;
                checkWinner();
                togglePlayer();
                if (currentPlayer === 'O') {
                    makeComputerMove();
                }
            }
        });
    });

    // Toggle between players (X and O)
    function togglePlayer() {
        currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    }

    // Check for a winner or a draw
    function checkWinner() {
        const winningCombos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  // Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  // Columns
            [0, 4, 8], [2, 4, 6]              // Diagonals
        ];

        for (const combo of winningCombos) {
            const [a, b, c] = combo;
            if (board[a] && board[a] === board[b] && board[a] === board[c]) {
                gameEnded = true;
                status.textContent = `Player ${board[a]} wins!`;
                return;
            }
        }

        if (board.every(cell => cell !== '')) {
            gameEnded = true;
            status.textContent = 'It\'s a draw!';
        }
    }

    // Make a random move for the computer player
    function makeComputerMove() {
        const availableSlots = board.reduce((acc, cell, index) => {
            if (cell === '') {
                acc.push(index);
            }
            return acc;
        }, []);

        if (availableSlots.length > 0) {
            const randomIndex = Math.floor(Math.random() * availableSlots.length);
            const computerMoveIndex = availableSlots[randomIndex];
            const computerMoveCell = cells[computerMoveIndex];
            computerMoveCell.textContent = currentPlayer;
            board[computerMoveIndex] = currentPlayer;
            checkWinner();
            togglePlayer();
        }
    }
});