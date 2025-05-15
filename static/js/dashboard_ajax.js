
document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-user");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const userId = this.dataset.userId;

            fetch(`/delete_user/${userId}`, {
                method: "DELETE"
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById(`user-row-${userId}`).remove();
                } else {
                    alert("Erreur lors de la suppression.");
                }
            });
        });
    });
});
