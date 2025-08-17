<script lang="ts">
    import MemoCard from "$lib/components/MemoCard.svelte";
    import MemoPlus from "$lib/components/MemoPlus.svelte";
    import type { Memo } from "$lib/types";
    import type { PageData } from "./$types";

    export let data: PageData;

    $: memos = data.memos;
</script>

<div class="grid grid-cols-7">
    {#each memos as memo (memo.id)}
        <MemoCard memo={memo} />
    {/each}
    <MemoPlus />
</div>