// Timeline page — loads posts via GET and creates them via POST without a full page reload.

const API_URL = "/api/timeline_post";

const form = document.getElementById("timeline-form");
const postsContainer = document.getElementById("timeline-posts");
const loadingEl = document.getElementById("timeline-loading");
const emptyEl = document.getElementById("timeline-empty");
const errorEl = document.getElementById("timeline-form-error");

function gravatarUrl(email) {
    const normalized = String(email || "").trim().toLowerCase();
    if (!normalized || typeof window.md5 !== "function") {
        return "https://www.gravatar.com/avatar/?d=mp&s=96";
    }

    const hash = window.md5(normalized);
    return `https://www.gravatar.com/avatar/${hash}?d=identicon&s=96`;
}

function formatDate(value) {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
        return value;
    }
    return date.toLocaleString(undefined, {
        dateStyle: "medium",
        timeStyle: "short",
    });
}

function createPostElement(post) {
    const article = document.createElement("article");
    article.className = "timeline-post";
    article.dataset.postId = post.id;

    const avatar = document.createElement("img");
    avatar.className = "timeline-avatar";
    avatar.src = gravatarUrl(post.email);
    avatar.alt = `Avatar for ${post.name}`;
    avatar.loading = "lazy";
    avatar.referrerPolicy = "no-referrer";

    const body = document.createElement("div");
    body.className = "timeline-post-body";

    const header = document.createElement("header");
    header.className = "timeline-post-header";

    const name = document.createElement("h3");
    name.className = "timeline-post-name";
    name.textContent = post.name;

    const meta = document.createElement("p");
    meta.className = "timeline-post-meta";
    meta.textContent = `${post.email} · ${formatDate(post.created_at)}`;

    const content = document.createElement("p");
    content.className = "timeline-post-content";
    content.textContent = post.content;

    header.appendChild(name);
    header.appendChild(meta);
    body.appendChild(header);
    body.appendChild(content);
    article.appendChild(avatar);
    article.appendChild(body);

    return article;
}

function renderPosts(posts) {
    postsContainer.innerHTML = "";

    if (!posts.length) {
        emptyEl.hidden = false;
        return;
    }

    emptyEl.hidden = true;
    posts.forEach((post) => {
        postsContainer.appendChild(createPostElement(post));
    });
}

function showFormError(message) {
    errorEl.textContent = message;
    errorEl.hidden = false;
}

function clearFormError() {
    errorEl.textContent = "";
    errorEl.hidden = true;
}

async function loadPosts() {
    loadingEl.hidden = false;
    emptyEl.hidden = true;

    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error("Could not load timeline posts.");
        }

        const data = await response.json();
        renderPosts(data.timeline_posts || []);
    } catch (error) {
        loadingEl.textContent = error.message;
    } finally {
        loadingEl.hidden = true;
    }
}

async function submitPost(event) {
    event.preventDefault();
    clearFormError();

    const submitButton = form.querySelector(".timeline-submit");
    submitButton.disabled = true;

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            body: new FormData(form),
        });

        if (!response.ok) {
            throw new Error("Could not create timeline post.");
        }

        const newPost = await response.json();
        emptyEl.hidden = true;
        postsContainer.prepend(createPostElement(newPost));
        form.reset();
    } catch (error) {
        showFormError(error.message);
    } finally {
        submitButton.disabled = false;
    }
}

if (form && postsContainer) {
    form.addEventListener("submit", submitPost);
    loadPosts();
}
