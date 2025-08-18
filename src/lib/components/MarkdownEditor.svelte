<script lang="ts">
    import "highlight.js/styles/github-dark.css";
    import { markdownParser } from "$lib/markdown";
    import { debounce } from "$lib/utils";

    export let value: string = "";
    export let placeholder: string = "내용을 입력하세요...";
    
    let markdownRenderedText: string = "";
    let isModalOpen: boolean = false;

    const debouncedUpdate = debounce(async (text: string) => {
        if (text.trim()) {
            markdownRenderedText = await markdownParser.parse(text);
        } else {
            markdownRenderedText = "";
        }
    }, 300);

    $: if (value !== undefined) {
        debouncedUpdate(value);
    }

    function openModal() {
        isModalOpen = true;
    }

    function closeModal() {
        isModalOpen = false;
    }

</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<div
    class="w-64 h-64 p-4 bg-white border-gray-50 border-2 cursor-pointer rounded-4xl m-4 hover:border-gray-100 hover:border-3 transition duration-150 ease-out break-words"
    on:click={openModal}
    role="button"
    tabindex="0"
>
    {value.length <= 100 ? value : value.substring(0, 100) + "..."} 
</div>

{#if isModalOpen}
<!-- svelte-ignore a11y_no_static_element_interactions -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<div class="fixed inset-0 bg-black/70 z-40 flex flex-col items-center justify-center">
    <div class="w-[80vw] h-[80vh] bg-white border-gray-50 border-4 rounded-3xl z-50 p-4 grid grid-cols-2 gap-4">
        <textarea 
            class="resize-none focus:outline-none focus:ring-gray-200 focus:ring-2 transition duration-150 ease-out h-full overflow-auto" 
            bind:value={value}
            {placeholder}
        ></textarea>
        <div class="prose h-full overflow-y-auto overflow-x-hidden break-words">
            {@html markdownRenderedText}
        </div>
    </div>

    <div class="flex justify-end w-[80vw] mt-4">
        <button
            class="bg-black/20 text-white m-2 px-8 py-4 text-lg font-bold rounded-2xl cursor-pointer hover:bg-white/10 transition duration-150 ease-out"
            on:click={closeModal}>
            닫기
        </button>
    </div>
</div>
{/if}

<style>
    :global(.prose pre) {
        background-color: transparent;
    }
</style>