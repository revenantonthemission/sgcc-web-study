<script lang="ts">
    import { marked } from "marked";

    let isModalOpen: boolean = false;
    let memoText: string = "";
    $: markdownRenderedMemoText = marked(memoText);
</script>