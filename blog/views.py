from django.shortcuts import render
from posts import models as post_models
from users import models as user_models

# Create your views here.

def firstPage(requist):
    
    # posts = post_models.Post.objects.all().order_by('-created_at')


    # image_urls = []

    # for post in posts:
    #     print(f"--- Checking Post: {post.title or 'Untitled'} (ID: {post.pk}) ---")
        
    #     # Efficiently select only the 'image' blocks and iterate
    #     # Note: Using .prefetch_related('content_blocks') before the loop 
    #     # would make this even more efficient for a large number of posts.
    #     image_blocks = post.content_blocks.filter(content_type='image')
        
    #     if not image_blocks.exists():
    #         print("    No image blocks found.")
    #         continue # Move to the next post
            
    #     for block in image_blocks:
    #         # The .url attribute provides the public URL to the file
    #         if block.media_file:
    #             url = block.media_file.url
    #             image_urls.append({
    #                 'post_id': post.pk,
    #                 'block_order': block.order,
    #                 'url': url
    #             })
    #             print(f"    ✅ Image URL (Order {block.order}): {url}")
    #         else:
    #             print(f"    ⚠️ Block {block.order} is an 'image' type but has no file saved.")

    # print("\n--- Summary of all Image URLs ---")
    # for item in image_urls:
    #         print(f"Post {item['post_id']} - Block {item['block_order']}: {item['url']}")
    users = user_models.User.objects.all()
    posts = post_models.Post.objects.all().order_by('-created_at').prefetch_related(
        'content_blocks'
    ).select_related('user')
    
    context = {
        'posts': posts, 
    }
    return render(requist , 'first.html', context)