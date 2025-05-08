<script>
  let count = $state(0);
  
  function increment() {
    count += 1;
  }
  function decrement() {
    count -= 1;
  }
  function reset() {
    count = 0;
  }
</script>

<button onclick={increment}>
  Clicked {count} {count === 1 ? 'time' : 'times'}
</button>