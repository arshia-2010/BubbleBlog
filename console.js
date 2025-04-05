const { data, error } = await supabase.auth.signInWithPassword({ email, password });

if (error) {
    console.error("Login Error:", error);
    alert("Login failed: " + error.message);
} else {
    console.log("Login Successful", data);
    window.location.href = "blog.html";
}
