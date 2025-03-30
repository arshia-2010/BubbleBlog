document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const email = document.getElementById("login-email").value;
        const password = document.getElementById("login-password").value;

        try {
            // Login logic using Supabase or Firebase
            const { data, error } = await supabase.auth.signInWithPassword({
                email: email,
                password: password
            });

            if (error) {
                throw new Error(error.message);
            }

            alert("Login successful! Redirecting to the blog page...");
            window.location.href = "blog.html"; // Redirect after successful login

        } catch (error) {
            console.error("Login error:", error.message);
            alert("Login failed: " + error.message);
        }
    });
});
