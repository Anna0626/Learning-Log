# movieguid

> 날짜: 2026-02-03
> 원본 노션: [링크](https://www.notion.so/movieguid-2fcb28703eb080698e3be81f6023de45)

---

```java
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <title>Watchlist</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>

  <!-- ===== Header ===== -->
  <nav class="header">
    <div class="header-inner">
      <!-- Left: 로고 + 메뉴 -->
      <div class="header-left">
        <a href="#" class="brand">
          <img src="images/logo.png" alt="Logo" class="brand-logo" />
          <span class="brand-name">MovieGuide</span>
        </a>

        <div class="header-nav">
          <button class="nav-link">추천</button>
          <button class="nav-link">Top 100</button>
          <button class="nav-link">Wishlist</button>
        </div>
      </div>

      <!-- Right: 로그인/회원가입 -->
      <div class="header-actions">
        <button class="btn btn-ghost">로그인</button>
        <button class="btn btn-primary">회원가입</button>
      </div>
    </div>
  </nav>

  <!-- ===== Main Container ===== -->
  <div class="container">

    <!-- Watchlist Header -->
    <div class="watchlist-header">
      <div class="title-row">
        <img src="./images/bookmark.png" width="30" alt="Bookmark" />
        <h1>보고 싶은 영화</h1>
      </div>
      <p class="subtitle">나중에 볼 영화를 저장해두세요</p>
    </div>

    <!-- Empty State -->
    <div class="empty-state">
      <svg class="icon-film" viewBox="0 0 24 24" fill="none">
        <rect x="2" y="2" width="20" height="20" rx="2" stroke="currentColor"/>
        <path d="M7 2v20M17 2v20" stroke="currentColor"/>
      </svg>
      <h2>저장된 영화가 없습니다</h2>
      <p>영화 카드의 + 버튼을 눌러 보고 싶은 영화를 추가해보세요</p>
    </div>

    <!-- Watchlist Content -->
    <div class="watchlist-content">
      <div class="count-text">총 3개의 영화</div>
      <div class="movie-grid">
        <div class="movie-card">
          <img src="images/images.jpg" alt="Movie Poster" />
          <div class="movie-info">
            <h3>Movie Title 1</h3>
          </div>
        </div>
        <div class="movie-card">
          <img src="images/images.jpg" alt="Movie Poster" />
          <div class="movie-info">
            <h3>Movie Title 2</h3>
            <h4>vote_average</h4>
            <h4>release_year</h4>
            <h4>genre_ids</h4>
          </div>
        </div>
      </div>
    </div>

  </div>
</body>
</html>

```

```java
/* Reset */
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: #0f0f1e;
  color: white;
}

/* ================= Header ================= */
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(7, 10, 22, 0.85);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #333;
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 14px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: white;
}

.brand-logo {
  width: 28px;
  height: 28px;
  object-fit: contain;
}

.brand-name {
  font-weight: 700;
  letter-spacing: 0.2px;
}

/* Header Left / Nav */
.header-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 12px;
}

.nav-link {
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
}

.nav-link.active {
  font-weight: bold;
}

/* Header Right / Buttons */
.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn {
  padding: 8px 12px;
  border-radius: 10px;
  font-weight: 600;
  border: 1px solid transparent;
  cursor: pointer;
}

.btn-ghost {
  background: transparent;
  color: white;
}

.btn-primary {
  background: #e94560;
  color: white;
}

/* ================= Container ================= */
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 16px;
}

/* Watchlist Header */
.watchlist-header .title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: -22px;
}

.watchlist-header .title-row h1 {
  font-size: 32px;
  font-weight: bold;
}

.watchlist-header .subtitle {
  color: #9ca3af;
}

/* ================= Empty State ================= */
.empty-state {
  text-align: center;
  padding: 80px 0;
}

.empty-state h2 {
  font-size: 20px;
  font-weight: 600;
  color: #9ca3af;
  margin-bottom: 8px;
}

.empty-state p {
  color: #6b7280;
}

.icon-film {
  width: 64px;
  height: 64px;
  color: #6b7280;
  margin-bottom: 16px;
}

/* ================= Watchlist Content ================= */
.count-text {
  margin-bottom: 16px;
  font-size: 14px;
  color: #9ca3af;
}

.movie-grid {
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(2, 1fr);
}

@media (min-width: 640px) {
  .movie-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (min-width: 768px) {
  .movie-grid { grid-template-columns: repeat(4, 1fr); }
}
@media (min-width: 1024px) {
  .movie-grid { grid-template-columns: repeat(5, 1fr); }
}

.movie-card {
  background-color: #1c1c3a;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.movie-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
}

.movie-card img {
  width: 100%;
  display: block;
}

.movie-info {
  padding: 12px;
}

.movie-info h3 {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.3;
}

```

```java
let currentPage = 'top100';
let user = null;
let watchlist = [];

const nav = document.getElementById('navigation');
const content = document.getElementById('content');

function renderNav() {
  nav.innerHTML = `
    <button onclick="navigate('top100')">Top100</button>
    <button onclick="navigate('watchlist')">Watchlist</button>
    <button onclick="navigate('profile')">Profile</button>
    ${
      user
        ? `<button onclick="logout()">Logout</button>`
        : `<button onclick="openLogin()">Login</button>`
    }
  `;
}

function renderPage() {
  if (currentPage === 'top100') {
    content.innerHTML = `<h1>Top 100 Movies</h1>`;
  }

  if (currentPage === 'home') {
    content.innerHTML = `<h1>Welcome, ${user.name}</h1>`;
  }

  if (currentPage === 'watchlist') {
    // watchlist 페이지일 때
    updateWatchlistView();
  }

  if (currentPage === 'profile') {
    if (!user) {
      openLogin();
      return;
    }
    content.innerHTML = `
      <h1>Profile</h1>
      <p>Email: ${user.email}</p>
    `;
  }
}


function navigate(page) {
  if (!user && (page === 'profile' || page === 'home')) {
    openLogin();
    return;
  }
  currentPage = page;
  renderPage();
}

/* Auth */
function login() {
  const email = loginEmail.value;
  user = {
    id: '1',
    email,
    name: email.split('@')[0],
    preferredGenres: [],
    dislikedGenres: []
  };
  closeModals();
  currentPage = 'home';
  renderNav();
  renderPage();
}

function signup() {
  const name = signupName.value;
  const email = signupEmail.value;
  user = {
    id: Date.now().toString(),
    email,
    name,
    preferredGenres: [],
    dislikedGenres: []
  };
  closeModals();
  currentPage = 'home';
  renderNav();
  renderPage();
}

function logout() {
  user = null;
  watchlist = [];
  currentPage = 'top100';
  renderNav();
  renderPage();
}

/* Modal */
function openLogin() {
  loginModal.classList.remove('hidden');
  signupModal.classList.add('hidden');
}

function openSignup() {
  signupModal.classList.remove('hidden');
  loginModal.classList.add('hidden');
}

function closeModals() {
  loginModal.classList.add('hidden');
  signupModal.classList.add('hidden');
}


function updateWatchlistView() {
  const emptyState = document.querySelector(".empty-state");
  const watchlistContent = document.querySelector(".watchlist-content");

  if (watchlist.length === 0) {
    // 영화 없음
    emptyState.style.display = "block";
    watchlistContent.style.display = "none";
  } else {
    // 영화 있음
    emptyState.style.display = "none";
    watchlistContent.style.display = "block";
  }
}




/* Init */
renderNav();
renderPage();

```

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/cb3b2870-3eb0-815c-99e6-0003045e9130/bb510985-515c-4ea4-b4e3-35a42771af16/KakaoTalk_20260202_162339154.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466T7LX7GR6%2F20260204%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260204T132822Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEE0aCXVzLXdlc3QtMiJIMEYCIQC0kaRFw9L4KOZ3UmJaJDnpjB0b3DGXJKO6dsYsivyoyQIhAJy%2BL63XKaK1HXXUatC823O%2B467JcgGt5q04L1PCeYxLKv8DCBYQABoMNjM3NDIzMTgzODA1Igw35%2FDSoeEnbi%2B2UDwq3ANQgAU8ULvgnqHQUKoDH5ClWJJZQWuYkjc7w1Kcnd4cj0j2bUrDzv%2FmYdS%2FfTLx6WHxEpXzTuTanZtg5xenUgHCGWN2IztHvZU4qAtjN3rblQp9ZdDGfXzc0dfW5%2Fe22JAEH%2FDnd1YSgZ10SoleOoqORAi0BTVDp0wDZmbtaQOLrQiYLKYhC9dU%2FUfSVb%2FgUR%2FSITWytAp36VVAKSKl8L%2FVTD4nWoFZ9mVR9D7ob%2FeYanrxr89HdaqgZ74b3NFY8p1wEG5DUrKAAkKMdAIUQiBKSa7ukAIZDsDkX3en4kmWqDD%2F1K0rx4jVQqXhRszGv0QH6WFO4KdscenN6oTqA5OUQ3lQN0Dp%2F%2FFgfWttsxdwG4mLubIDVANKd4k7kbnt6EGMsNus99mC7y3aDSTpXepYI2ozwGBq3nVA6VMnSPCp7B15isXoPB4Gkc9eHW%2Fvdw7BUGOQEiUR4WhUCrI94%2FTfLMVLzF6zJf%2BPk%2F84b9pcfLITs4KkSGLSZnWJRvtAkmOcSbLFCJZrPb3Tiquuc%2FoeNfC1KBJ74aVNx%2BC8fUrz6tGvx9H4tp523eZtGdz%2B%2FwpxUb7%2BqgM3nz9wY8pSFKCkxnr%2Fc2nnpxgfTOl%2FN1RCA6Uq5sXKLZ1S%2FCZYwDCljY3MBjqkAZbYZOAc7oKQ7kwNvtOlUfBXUP6%2FbdrQLqsG%2BIxzbKq56yfjoTG8HoVWgtPgop70tjB6FvGOB7WjhM9Q6gy5NqNLxntXs6D%2FQLY7rULvddrM8KNrCLzeCFEwHfZObfJKTxLOr4jikNzKTr3mAuztAsj7awoVJyCZ2w4T%2Fdi02ga0EGRa6X7HyvL%2FrAQKnYKgexXo9FKhMgRobqWynkEBtlzlPoGh&X-Amz-Signature=92af155f84f02c9e48f514e81ec12f0a01d7dc156b2bdac43a00edf4e2b81a07&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/cb3b2870-3eb0-815c-99e6-0003045e9130/2ec626f1-93db-4f2c-8610-e612f8013f8b/KakaoTalk_20260202_162633774.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466T7LX7GR6%2F20260204%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260204T132822Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEE0aCXVzLXdlc3QtMiJIMEYCIQC0kaRFw9L4KOZ3UmJaJDnpjB0b3DGXJKO6dsYsivyoyQIhAJy%2BL63XKaK1HXXUatC823O%2B467JcgGt5q04L1PCeYxLKv8DCBYQABoMNjM3NDIzMTgzODA1Igw35%2FDSoeEnbi%2B2UDwq3ANQgAU8ULvgnqHQUKoDH5ClWJJZQWuYkjc7w1Kcnd4cj0j2bUrDzv%2FmYdS%2FfTLx6WHxEpXzTuTanZtg5xenUgHCGWN2IztHvZU4qAtjN3rblQp9ZdDGfXzc0dfW5%2Fe22JAEH%2FDnd1YSgZ10SoleOoqORAi0BTVDp0wDZmbtaQOLrQiYLKYhC9dU%2FUfSVb%2FgUR%2FSITWytAp36VVAKSKl8L%2FVTD4nWoFZ9mVR9D7ob%2FeYanrxr89HdaqgZ74b3NFY8p1wEG5DUrKAAkKMdAIUQiBKSa7ukAIZDsDkX3en4kmWqDD%2F1K0rx4jVQqXhRszGv0QH6WFO4KdscenN6oTqA5OUQ3lQN0Dp%2F%2FFgfWttsxdwG4mLubIDVANKd4k7kbnt6EGMsNus99mC7y3aDSTpXepYI2ozwGBq3nVA6VMnSPCp7B15isXoPB4Gkc9eHW%2Fvdw7BUGOQEiUR4WhUCrI94%2FTfLMVLzF6zJf%2BPk%2F84b9pcfLITs4KkSGLSZnWJRvtAkmOcSbLFCJZrPb3Tiquuc%2FoeNfC1KBJ74aVNx%2BC8fUrz6tGvx9H4tp523eZtGdz%2B%2FwpxUb7%2BqgM3nz9wY8pSFKCkxnr%2Fc2nnpxgfTOl%2FN1RCA6Uq5sXKLZ1S%2FCZYwDCljY3MBjqkAZbYZOAc7oKQ7kwNvtOlUfBXUP6%2FbdrQLqsG%2BIxzbKq56yfjoTG8HoVWgtPgop70tjB6FvGOB7WjhM9Q6gy5NqNLxntXs6D%2FQLY7rULvddrM8KNrCLzeCFEwHfZObfJKTxLOr4jikNzKTr3mAuztAsj7awoVJyCZ2w4T%2Fdi02ga0EGRa6X7HyvL%2FrAQKnYKgexXo9FKhMgRobqWynkEBtlzlPoGh&X-Amz-Signature=89b6187130ca2aedaa3a2e4357b0c6167ee3884b99caa16fb60488d0293cf7ef&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

