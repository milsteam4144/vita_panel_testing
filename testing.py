import panel as pn

# Create a long text content
long_text = "This is a very long line of text that should cause horizontal scrolling. " * 10

# Create a custom HTML component with JavaScript
custom_html = f"""
<div id="scroll-container" style="width: 400px; height: 100px; overflow-x: auto; white-space: nowrap; border: 1px solid #ddd;">
    <div id="content">{long_text}</div>
</div>

<script>
    setTimeout(function() {{
        var container = document.getElementById('scroll-container');
        var content = document.getElementById('content');
        if (content.offsetWidth > container.offsetWidth) {{
            container.style.overflowX = 'scroll';
        }}
    }}, 100);
</script>
"""

# Create a pane with the custom HTML
custom_pane = pn.pane.HTML(custom_html, width=420, height=120)

# Create a template
template = pn.template.FastListTemplate(
    title="Scrollable Text Example",
    main=[custom_pane],
)

# Show the result
template.servable()