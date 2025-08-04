<script lang="ts">
    import { Plus } from "@lucide/svelte";
    import { createMemo } from "$lib/api";
    import { invalidateAll } from "$app/navigation";

    async function handleClick() {
        createMemo("New memo", "New memo");
        await invalidateAll();
    }
</script>

<button class="w-64 h-64 p-4 bg-white flex border-gray-50 border-2 items-center justify-center cursor-pointer rounded-4xl m-4 hover:border-gray-100 hover:border-3 transition duration-150 ease-out" on:click={handleClick}>
    <Plus class="h-12 w-12"/>
</button>