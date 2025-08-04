<script lang="ts">
    import "highlight.js/styles/github-dark.css";
    import { markdownParser } from "$lib/markdown";
    import { debounce } from "$lib/utils";
    import type { Memo } from "$lib/types";
    import { updateMemo, deleteMemo } from "$lib/api";

    export let memo: Memo;
    
    let memoText: string = memo.content;
    let memoTitle: string = memo.title;
    let markdownRenderedMemoText: string = "";
    let isModalOpen: boolean = false;

    const debouncedUpdate = debounce(async (text: string) => {
        if (text.trim()) {
            markdownRenderedMemoText = await markdownParser.parse(text);
        } else {
            markdownRenderedMemoText = "";
        }
    }, 300);

    $: if (memoText !== undefined) {
        debouncedUpdate(memoText);
    }

    function openModal() {
        memoText = memo.content;
        memoTitle = memo.title;
        isModalOpen = true;
    }

    function closeModal() {
        isModalOpen = false;
    }

    async function saveMemo() {
        try {
            const updatedMemo = await updateMemo(memo.id, {
                title: memoTitle,
                content: memoText
            });
            memo = updatedMemo;
            closeModal();
        } catch (error) {
            console.error('Failed to update memo:', error);
            alert('메모 저장에 실패했습니다.');
        }
    }

    async function handleDeleteMemo() {
        if (confirm('정말로 이 메모를 삭제하시겠습니까?')) {
            try {
                await deleteMemo(memo.id);
                location.reload();
            } catch (error) {
                console.error('Failed to delete memo:', error);
                alert('메모 삭제에 실패했습니다.');
            }
        }
    }
</script>

<div
    class="w-64 h-64 p-4 bg-white border-gray-50 border-2 cursor-pointer rounded-4xl m-4 hover:border-gray-100 hover:border-3 transition duration-150 ease-out break-words"
    on:click={openModal}
    on:keydown={(e) => e.key === 'Enter' && openModal()}
    role="button"
    tabindex="0"
>
    <div class="font-bold text-lg mb-2 truncate">{memo.title}</div>
    <div class="text-sm text-gray-600">
        {memo.content.length <= 80 ? memo.content : memo.content.substring(0, 80) + "..."}
    </div>
</div>

{#if isModalOpen}
<div class="fixed inset-0 bg-black/70 z-40 flex flex-col items-center justify-center">
    <div class="w-[80vw] h-[80vh] bg-white border-gray-50 border-4 rounded-3xl z-50 p-4 flex flex-col gap-4">
        <input 
            class="text-xl font-bold border-b-2 border-gray-200 pb-2 focus:outline-none focus:border-gray-400"
            bind:value={memoTitle}
            placeholder="메모 제목"
        />
        <div class="flex-1 grid grid-cols-2 gap-4 min-h-0">
            <textarea 
                class="resize-none focus:outline-none focus:ring-gray-200 focus:ring-2 transition duration-150 ease-out h-full min-h-0 verflow-y-auto" 
                bind:value={memoText}
                placeholder="메모 내용을 입력하세요..."
            ></textarea>
            <div class="prose h-full min-h-0 overflow-y-auto overflow-x-hidden break-words">
                {@html markdownRenderedMemoText}
            </div>
        </div>
    </div>

    <div class="flex justify-end w-[80vw] mt-4">
        <button
            class="bg-red-500/20 text-white m-2 px-8 py-4 text-lg font-bold rounded-2xl cursor-pointer hover:bg-red-500/30 transition duration-150 ease-out"
            on:click={handleDeleteMemo}>
            삭제
        </button>
        <button
            class="bg-black/20 text-white m-2 px-8 py-4 text-lg font-bold rounded-2xl cursor-pointer hover:bg-white/10 transition duration-150 ease-out"
            on:click={closeModal}>
            닫기
        </button>
        <button
            class="bg-blue-500/20 text-white m-2 px-8 py-4 text-lg font-bold rounded-2xl cursor-pointer hover:bg-blue-500/30 transition duration-150 ease-out"
            on:click={saveMemo}>
            저장
        </button>
    </div>
</div>
{/if}

<style>
    :global(.prose pre) {
        background-color: transparent;
    }
</style>