document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-recipe').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            const recipeId = this.dataset.recipeId;
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            fetch(`/delete_saved_recipe/${recipeId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Remove the recipe from the DOM
                    const recipeCard = document.getElementById(`recipe-${recipeId}`);
                    if (recipeCard) {
                        recipeCard.remove();
                    }
                    displayMessage('Recipe has been deleted from your saved recipes.', 'success');
                } else {
                    displayMessage('Error deleting recipe.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                displayMessage('Error deleting recipe.', 'error');
            });
        });
    });

    function displayMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
        messageDiv.innerText = message;
        document.body.appendChild(messageDiv);

        setTimeout(() => {
            messageDiv.remove();
        }, 3000); // Message disappears after 3 seconds
    }
});
