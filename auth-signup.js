document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signup-form");

    signupForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const email = document.getElementById("signup-email").value;
        const password = document.getElementById("signup-password").value;

        try {
            // Sign-up logic using Supabase or Firebase
            const { data, error } = await supabase.auth.signUp({
                email: email,
                password: password
            });
            
            if (error) {
                throw new Error(error.message);
            }

            alert("Sign-up successful! Redirecting to the blog page...");
            window.location.href = "blog.html"; // Redirect after successful sign-up

        } catch (error) {
            console.error("Sign-up error:", error.message);
            alert("Sign-up failed: " + error.message);
        }
    });
});
