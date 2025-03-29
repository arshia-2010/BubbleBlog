/**
 * Blog Application - Frontend JavaScript
 * Features: Authentication, Post Management, Error Handling
 */

// Configuration
const BLOG_PASSWORD = "blog123"; // Frontend-only authentication (not secure for production)
const MAX_IMAGE_SIZE = 2 * 1024 * 1024; // 2MB

// DOM Ready Handler
document.addEventListener("DOMContentLoaded", function() {
    try {
        console.log("Initializing blog application...");
        checkAuth();
        setupEventListeners();
    } catch (initError) {
        console.error("Application initialization failed:", initError);
        showGlobalError("System error. Please refresh the page.");
    }
});

// Authentication Functions
function checkAuth() {
    try {
        if (shouldCheckAuth()) {
            const isAuthenticated = localStorage.getItem("authenticated") === "true";
            if (!isAuthenticated) {
                console.warn("Unauthorized access attempt to protected page");
                window.location.href = "index.html";
            }
        }
    } catch (authError) {
        console.error("Authentication check failed:", authError);
        // Allow access but log the error
    }
}

function shouldCheckAuth() {
    const protectedPages = ["blog.html", "create.html", "editpost.html"];
    return protectedPages.some(page => window.location.pathname.endsWith(page));
}

// Core Event Listeners
function setupEventListeners() {
    try {
        // Login Page
        if (document.getElementById("loginForm")) {
            setupLoginForm();
        }

        // Blog Page
        if (document.getElementById("logoutBtn")) {
            setupBlogPage();
        }

        // Create/Edit Page
        if (document.getElementById("blogForm")) {
            setupPostForm();
        }

        // View Post Page
        if (document.getElementById("postContainer")) {
            setupViewPost();
        }
    } catch (eventError) {
        console.error("Event setup failed:", eventError);
    }
}

// Login Functionality
function setupLoginForm() {
    const loginForm = document.getElementById("loginForm");
    const loginError = document.getElementById("loginError");
    
    loginForm.addEventListener("submit", function(e) {
        e.preventDefault();
        try {
            const password = document.getElementById("password").value.trim();
            
            if (!password) {
                throw new Error("Password cannot be empty");
            }
            
            if (password === BLOG_PASSWORD) {
                console.log("User authenticated successfully");
                localStorage.setItem("authenticated", "true");
                window.location.href = "blog.html";
            } else {
                console.warn("Failed login attempt");
                throw new Error("Incorrect password. Please try again.");
            }
        } catch (loginError) {
            console.error("Login error:", loginError);
            loginError.textContent = loginError.message;
        }
    });
}

// Blog Page Functions
function setupBlogPage() {
    // Navigation
    document.getElementById("logoutBtn").addEventListener("click", handleLogout);
    document.getElementById("createBtn").addEventListener("click", () => {
        window.location.href = "create.html";
    });

    // Load posts
    try {
        loadBlogPosts();
    } catch (loadError) {
        console.error("Failed to load posts:", loadError);
        document.getElementById("blogList").innerHTML = `
            <div class="error-message">
                Failed to load posts. Please try again later.
            </div>
        `;
    }
}

function handleLogout() {
    try {
        console.log("User logging out");
        localStorage.removeItem("authenticated");
        window.location.href = "index.html";
    } catch (logoutError) {
        console.error("Logout failed:", logoutError);
    }
}

// Post Management
function loadBlogPosts() {
    const blogList = document.getElementById("blogList");
    blogList.innerHTML = "";
    
    try {
        const posts = JSON.parse(localStorage.getItem("blogPosts")) || [];
        
        if (posts.length === 0) {
            blogList.innerHTML = `
                <div class="empty-state">
                    <p>No blog posts yet.</p>
                    <button onclick="window.location.href='create.html'">
                        Create your first post!
                    </button>
                </div>
            `;
            return;
        }
        
        posts.forEach((post, index) => {
            try {
                const blogCard = createPostCard(post, index);
                blogList.appendChild(blogCard);
            } catch (cardError) {
                console.error(`Error rendering post ${index}:`, cardError);
            }
        });
    } catch (parseError) {
        console.error("Error parsing blog posts:", parseError);
        throw new Error("Could not load posts");
    }
}

function createPostCard(post, index) {
    const blogCard = document.createElement("div");
    blogCard.className = "blog-card";
    
    let imageHtml = "";
    if (post.image) {
        imageHtml = `
            <div class="image-container">
                <img src="${post.image}" 
                     alt="${post.title}" 
                     class="blog-image"
                     onerror="this.style.display='none'">
            </div>
        `;
    }
    
    blogCard.innerHTML = `
        ${imageHtml}
        <div class="blog-content">
            <h2 class="blog-title">${post.title}</h2>
            <p class="blog-date">
                ${new Date(post.date).toLocaleDateString()}
                ${new Date(post.date).toLocaleTimeString()}
            </p>
            <p class="blog-excerpt">${post.content.substring(0, 100)}...</p>
            <div class="card-actions">
                <button onclick="viewPost(${index})">Read More</button>
                <button onclick="editPost(${index})">Edit</button>
            </div>
        </div>
    `;
    
    return blogCard;
}

// Post Creation/Editing
function setupPostForm() {
    try {
        // Back button
        if (document.getElementById("backBtn")) {
            document.getElementById("backBtn").addEventListener("click", () => {
                window.location.href = "blog.html";
            });
        }

        // Image preview
        setupImagePreview();

        // Form submission
        const blogForm = document.getElementById("blogForm");
        blogForm.addEventListener("submit", handlePostSubmission);
        
        // Check if editing existing post
        const urlParams = new URLSearchParams(window.location.search);
        const editIndex = urlParams.get('edit');
        
        if (editIndex !== null) {
            loadPostForEdit(editIndex);
        }
    } catch (formError) {
        console.error("Post form setup failed:", formError);
    }
}

function setupImagePreview() {
    const imageInput = document.getElementById("image");
    const imagePreview = document.getElementById("imagePreview");
    
    imageInput.addEventListener("change", function() {
        try {
            const file = this.files[0];
            if (!file) return;
            
            // Validate image
            if (!file.type.startsWith('image/')) {
                throw new Error("Please select an image file");
            }
            
            if (file.size > MAX_IMAGE_SIZE) {
                throw new Error(`Image must be less than ${MAX_IMAGE_SIZE/1024/1024}MB`);
            }
            
            const reader = new FileReader();
            
            reader.onload = function() {
                imagePreview.innerHTML = `
                    <img src="${this.result}" alt="Preview">
                    <button onclick="clearImagePreview()" class="remove-image">
                        Remove Image
                    </button>
                `;
            };
            
            reader.onerror = function() {
                throw new Error("Failed to read image file");
            };
            
            reader.readAsDataURL(file);
        } catch (previewError) {
            console.error("Image preview error:", previewError);
            imagePreview.innerHTML = `
                <div class="error">${previewError.message}</div>
            `;
            imageInput.value = "";
        }
    });
}

function clearImagePreview() {
    try {
        document.getElementById("imagePreview").innerHTML = "";
        document.getElementById("image").value = "";
    } catch (error) {
        console.error("Error clearing image preview:", error);
    }
}

function handlePostSubmission(e) {
    e.preventDefault();
    try {
        const title = document.getElementById("title").value.trim();
        const content = document.getElementById("content").value.trim();
        
        if (!title || !content) {
            throw new Error("Title and content are required");
        }
        
        const imageInput = document.getElementById("image");
        let imageUrl = "";
        if (imageInput.files[0]) {
            imageUrl = URL.createObjectURL(imageInput.files[0]);
        }
        
        const urlParams = new URLSearchParams(window.location.search);
        const editIndex = urlParams.get('edit');
        
        const posts = JSON.parse(localStorage.getItem("blogPosts")) || [];
        const newPost = {
            title,
            content,
            image: imageUrl,
            date: new Date().toISOString()
        };
        
        if (editIndex !== null) {
            // Update existing post
            posts[editIndex] = newPost;
            console.log(`Updated post at index ${editIndex}`);
        } else {
            // Add new post
            posts.unshift(newPost);
            console.log("Created new post");
        }
        
        localStorage.setItem("blogPosts", JSON.stringify(posts));
        window.location.href = "blog.html";
    } catch (submissionError) {
        console.error("Post submission failed:", submissionError);
        showFormError(submissionError.message);
    }
}

function loadPostForEdit(index) {
    try {
        const posts = JSON.parse(localStorage.getItem("blogPosts")) || [];
        const post = posts[index];
        
        if (!post) {
            throw new Error("Post not found for editing");
        }
        
        document.getElementById("title").value = post.title;
        document.getElementById("content").value = post.content;
        
        if (post.image) {
            document.getElementById("imagePreview").innerHTML = `
                <img src="${post.image}" alt="Existing post image">
                <button onclick="clearImagePreview()" class="remove-image">
                    Remove Image
                </button>
            `;
        }
        
        document.querySelector("form button[type='submit']").textContent = "Update Post";
    } catch (editError) {
        console.error("Error loading post for edit:", editError);
        showFormError("Could not load post for editing");
        window.location.href = "blog.html";
    }
}

// View Post Functions
function setupViewPost() {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const postIndex = urlParams.get('post');
        
        if (postIndex !== null) {
            viewPost(postIndex);
        } else {
            throw new Error("No post specified");
        }
    } catch (viewError) {
        console.error("View post setup failed:", viewError);
        document.getElementById("postContainer").innerHTML = `
            <div class="error-message">
                Post could not be loaded. <a href="blog.html">Return to blog</a>
            </div>
        `;
    }
}

function viewPost(index) {
    try {
        const posts = JSON.parse(localStorage.getItem("blogPosts")) || [];
        const post = posts[index];
        
        if (!post) {
            throw new Error("Post not found");
        }
        
        const postContainer = document.getElementById("postContainer");
        let imageHtml = "";
        
        if (post.image) {
            imageHtml = `
                <div class="post-image">
                    <img src="${post.image}" alt="${post.title}"
                         onerror="this.style.display='none'">
                </div>
            `;
        }
        
        postContainer.innerHTML = `
            <article class="full-post">
                ${imageHtml}
                <h1>${post.title}</h1>
                <div class="post-meta">
                    ${new Date(post.date).toLocaleDateString()}
                    ${new Date(post.date).toLocaleTimeString()}
                </div>
                <div class="post-content">${post.content}</div>
                <div class="post-actions">
                    <button onclick="window.location.href='blog.html'">
                        Back to Blog
                    </button>
                    <button onclick="editPost(${index})">
                        Edit Post
                    </button>
                </div>
            </article>
        `;
    } catch (error) {
        console.error("Error viewing post:", error);
        throw error;
    }
}

function editPost(index) {
    window.location.href = `create.html?edit=${index}`;
}

// Utility Functions
function showFormError(message) {
    const errorDiv = document.createElement("div");
    errorDiv.className = "form-error";
    errorDiv.textContent = message;
    
    const form = document.getElementById("blogForm");
    const existingError = form.querySelector(".form-error");
    
    if (existingError) {
        existingError.replaceWith(errorDiv);
    } else {
        form.prepend(errorDiv);
    }
}

function showGlobalError(message) {
    const errorDiv = document.createElement("div");
    errorDiv.className = "global-error";
    errorDiv.innerHTML = `
        <p>${message}</p>
        <button onclick="location.reload()">Refresh Page</button>
    `;
    
    document.body.prepend(errorDiv);
}

// Global Error Handling
window.addEventListener('error', function(event) {
    console.error("Uncaught error:", {
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        error: event.error
    });
});

window.addEventListener('unhandledrejection', function(event) {
    console.error("Unhandled promise rejection:", event.reason);
});

// Make functions available globally
window.viewPost = viewPost;
window.editPost = editPost;
window.clearImagePreview = clearImagePreview;