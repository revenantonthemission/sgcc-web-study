<script>
  import { onMount } from 'svelte';
  import { fly, fade } from 'svelte/transition';
  
  let mounted = false;
  
  onMount(() => {
    mounted = true;
  });
  
  const features = [
    { title: 'Svelte 반응성', description: '상태 변화에 따른 자동 UI 업데이트', icon: '⚡' },
    { title: 'SvelteKit 라우팅', description: '파일 기반 라우팅 시스템', icon: '🛣️' },
    { title: '서버사이드 렌더링', description: 'SEO 최적화된 페이지 렌더링', icon: '🖥️' },
    { title: '컴포넌트 시스템', description: '재사용 가능한 UI 컴포넌트', icon: '🧩' },
    { title: '상태 관리', description: 'Svelte Store를 활용한 전역 상태', icon: '📦' },
    { title: 'API 라우트', description: 'SvelteKit의 서버사이드 API', icon: '🔗' },
    { title: '트랜지션 & 애니메이션', description: '부드러운 사용자 경험', icon: '✨' },
    { title: '반응형 디자인', description: '모든 디바이스에서 최적화', icon: '📱' }
  ];
</script>

<svelte:head>
  <title>할 일 관리 - 정보</title>
</svelte:head>

<div class="about-page">
  {#if mounted}
    <div class="hero" in:fade="{{ duration: 500 }}">
      <h1>SvelteKit 할 일 관리 앱</h1>
      <p class="hero-subtitle">
        Svelte와 SvelteKit의 모든 기능을 학습할 수 있는 종합적인 웹 애플리케이션
      </p>
    </div>
    
    <div class="features">
      <h2>구현된 기능들</h2>
      <div class="features-grid">
        {#each features as feature, i}
          <div 
            class="feature-card"
            in:fly="{{ y: 50, duration: 300, delay: i * 100 }}"
          >
            <div class="feature-icon">{feature.icon}</div>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        {/each}
      </div>
    </div>
    
    <div class="tech-stack" in:fly="{{ y: 50, duration: 500, delay: 800 }}">
      <h2>기술 스택</h2>
      <div class="tech-items">
        <div class="tech-item">
          <strong>Frontend</strong>
          <span>Svelte, SvelteKit, CSS3</span>
        </div>
        <div class="tech-item">
          <strong>State Management</strong>
          <span>Svelte Stores (writable, derived)</span>
        </div>
        <div class="tech-item">
          <strong>Routing</strong>
          <span>SvelteKit File-based Routing</span>
        </div>
        <div class="tech-item">
          <strong>API</strong>
          <span>SvelteKit Server Routes</span>
        </div>
        <div class="tech-item">
          <strong>Animations</strong>
          <span>Svelte Transitions & Animations</span>
        </div>
      </div>
    </div>
    
    <div class="learning-points" in:fly="{{ y: 50, duration: 500, delay: 1000 }}">
      <h2>학습 포인트</h2>
      <div class="learning-grid">
        <div class="learning-section">
          <h3>Svelte 핵심 개념</h3>
          <ul>
            <li>반응성 (Reactivity)</li>
            <li>컴포넌트 통신 (Props & Events)</li>
            <li>조건부 렌더링 & 반복</li>
            <li>바인딩 (Binding)</li>
            <li>생명주기 (Lifecycle)</li>
          </ul>
        </div>
        
        <div class="learning-section">
          <h3>SvelteKit 기능</h3>
          <ul>
            <li>파일 기반 라우팅</li>
            <li>레이아웃 시스템</li>
            <li>서버사이드 렌더링</li>
            <li>API 라우트</li>
            <li>빌드 최적화</li>
          </ul>
        </div>
        
        <div class="learning-section">
          <h3>고급 패턴</h3>
          <ul>
            <li>상태 관리 패턴</li>
            <li>에러 처리</li>
            <li>성능 최적화</li>
            <li>접근성 고려</li>
            <li>테마 시스템</li>
          </ul>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .about-page {
    max-width: 1000px;
    margin: 0 auto;
  }
  
  .hero {
    text-align: center;
    padding: 3rem 0;
    background: linear-gradient(135deg, var(--primary), var(--success));
    border-radius: 1rem;
    color: white;
    margin-bottom: 3rem;
  }
  
  .hero h1 {
    margin: 0 0 1rem 0;
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.125rem;
    opacity: 0.9;
    margin: 0;
  }
  
  .features {
    margin-bottom: 3rem;
  }
  
  .features h2 {
    text-align: center;
    color: var(--primary);
    margin-bottom: 2rem;
  }
  
  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }
  
  .feature-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1rem;
    padding: 2rem;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  
  .feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
  }
  
  .feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }
  
  .feature-card h3 {
    margin: 0 0 0.5rem 0;
    color: var(--primary);
  }
  
  .feature-card p {
    margin: 0;
    color: var(--text-light);
    font-size: 0.875rem;
    line-height: 1.5;
  }
  
  .tech-stack {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1rem;
    padding: 2rem;
    margin-bottom: 3rem;
  }
  
  .tech-stack h2 {
    text-align: center;
    color: var(--primary);
    margin-bottom: 2rem;
  }
  
  .tech-items {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }
  
  .tech-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    padding: 1rem;
    background: var(--bg);
    border-radius: 0.5rem;
  }
  
  .tech-item strong {
    color: var(--primary);
    font-size: 0.875rem;
  }
  
  .tech-item span {
    color: var(--text-light);
    font-size: 0.875rem;
  }
  
  .learning-points h2 {
    text-align: center;
    color: var(--primary);
    margin-bottom: 2rem;
  }
  
  .learning-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
  }
  
  .learning-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1rem;
    padding: 2rem;
  }
  
  .learning-section h3 {
    margin: 0 0 1rem 0;
    color: var(--primary);
  }
  
  .learning-section ul {
    margin: 0;
    padding-left: 1.5rem;
    list-style-type: none;
  }
  
  .learning-section li {
    position: relative;
    margin-bottom: 0.5rem;
    color: var(--text);
  }
  
  .learning-section li::before {
    content: '✓';
    position: absolute;
    left: -1.5rem;
    color: var(--success);
    font-weight: bold;
  }
</style>