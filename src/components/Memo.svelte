<script lang="ts">
    import { marked } from "marked";

    let isModalOpen: boolean = false;
    let memoText: string = "";
    let savedMemoText: string = "";
    $: markdownRenderedMemoText = marked(memoText);

    function openModal() {
        memoText= savedMemoText;
        isModalOpen = true;
    }

    function closeModal() {
        isModalOpen = false;
    }

    function saveMemo() {
        savedMemoText = memoText;
        closeModal();
    }
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<div
    class="w-64 h-64 p-4 bg-white border-gray-50 border-2 cursor-pointer rounded-4xl m-4 hover:border-gray-100 hover:border-3 transition duration-150 ease-out"
    on:click={openModal}
    role="button"
    tabindex="0"
>
    {savedMemoText.length <= 100 ? savedMemoText : savedMemoText.substring(0, 100) + "..."} 
</div>

{#if isModalOpen}
<!-- svelte-ignore a11y_no_static_element_interactions -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<div class="fixed inset-0 bg-black/70 z-40 flex flex-col items-center justify-center">
    <div class="w-[80vw] h-[80vh] bg-white border-gray-50 border-4 rounded-3xl z-50 p-4 grid grid-cols-2 gap-4">
        <textarea class="resize-none focus:outline-none focus:ring-gray-200 focus:ring-2 transition duration-150 ease-out" bind:value={memoText}>
            {savedMemoText}
        </textarea>
        <div class="prose">
            {@html markdownRenderedMemoText}
        </div>
    </div>

    <div class="flex justify-end w-[80vw] mt-4">
        <button
            class="bg-black/20 text-white m-2 px-8 py-4 text-lg font-bold rounded-2xl cursor-pointer hover:bg-white/10 transition duration-150 ease-out"
            on:click={closeModal}>
            닫기
        </button>
        <button
            class="bg-black/20 text-white m-2 px-8 py-4 text-lg font-bold rounded-2xl cursor-pointer hover:bg-white/10 transition duration-150 ease-out"
            on:click={saveMemo}>
            저장
        </button>
    </div>
</div>
{/if}