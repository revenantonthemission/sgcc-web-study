<script>
  import { page } from '$app/stores';
  
  $: status = $page.status;
  $: message = $page.error?.message || '알 수 없는 오류가 발생했습니다.';
</script>

<div class="error-page">
  <div class="error-content">
    <h1 class="error-code">{status}</h1>
    <h2 class="error-title">
      {status === 404 ? '페이지를 찾을 수 없습니다' : '오류가 발생했습니다'}
    </h2>
    <p class="error-message">{message}</p>
    <a href="/" class="home-link">홈으로 돌아가기</a>
  </div>
</div>

<style>
  .error-page {
    min-height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
  }
  
  .error-content {
    max-width: 500px;
    padding: 2rem;
  }
  
  .error-code {
    font-size: 4rem;
    color: var(--error);
    margin: 0 0 1rem 0;
    font-weight: bold;
  }
  
  .error-title {
    margin: 0 0 1rem 0;
    color: var(--text);
  }
  
  .error-message {
    color: var(--text-light);
    margin-bottom: 2rem;
  }
  
  .home-link {
    display: inline-block;
    background: var(--primary);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    text-decoration: none;
    transition: background-color 0.2s;
  }
  
  .home-link:hover {
    background: var(--primary-dark);
  }
</style>