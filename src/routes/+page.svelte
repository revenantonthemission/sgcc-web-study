<script lang="ts">
    import MemoCard from "$lib/components/MemoCard.svelte";
    import type { Memo } from "$lib/types";
    import type { PageData } from "./$types";

    export let data: PageData;

    $: memos = data.memos;
</script>

<div class="grid grid-cols-7">
    {#each memos as memo}
        <MemoCard memo={memo} />
    {/each}
</div>