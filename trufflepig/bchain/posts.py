import trufflepig.filters.textfilters as tftf


TRUFFLE_LINK = 'https://steemit.com/steemit/@smcaterpillar/trufflepig-introducing-the-artificial-intelligence-for-content-curation-and-minnow-support'
TRUFFLE_IMAGE_SMALL = '![trufflepig](https://raw.githubusercontent.com/SmokinCaterpillar/TrufflePig/master/img/trufflepig17_small.png)'
TRUFFLE_IMAGE = '![trufflepig](https://raw.githubusercontent.com/SmokinCaterpillar/TrufflePig/master/img/trufflepig17.png)'
QUOTE_MAX_LENGTH=256
TAGS = ['steemit', 'steem', 'minnowsupport', 'upvote', 'trufflepig']


def truffle_comment(reward, votes, rank, topN_link, truffle_link=TRUFFLE_LINK, truffle_image_small=TRUFFLE_IMAGE_SMALL):
    post = """**Congratulations!** Your post has been selected as quality content that deserves more attention.
    
I upvoted your contribution because to my mind your post is at least **{reward} SBD** worth and should have received **{votes} votes**. It's now up to the lovely Steemit community to make this come true. By the way, your post is listed on rank {rank} of all truffles found today! You can find the [top daily truffle picks here.]({topN_link})
    
I am `TrufflePig`, an Artificial Intelligence Bot that helps minnows and content curators using Machine Learning. I was created and am being maintained by @smcaterpillar. If you are curious how I select content, [you can find an explanation here!]({truffle_link})
    
Have a nice day and sincerely yours,
{truffle_image_small}
*`TrufflePig`*

PS: Upvoting and resteeming my posts and comments will support paying for server costs and further development, thank you ;-)
    """

    return post.format(reward=int(reward), votes=int(votes), topN_link=topN_link,
                       truffle_link=truffle_link, rank=rank,
                       truffle_image_small=truffle_image_small)


def topN_list(topN_authors, topN_permalinks, topN_titles, topN_filtered_bodies, topN_rewards, topN_votes,
               quote_max_length):

    topN_entry="""{rank}. [{title}](https://steemit.com/@{author}/{permalink})  --  **by @{author} with an estimated worth of {reward:d} SBD and {votes:d} votes**
    
    {quote}

"""

    result_string = ""

    iterable = zip(topN_authors, topN_permalinks, topN_titles,
                   topN_filtered_bodies, topN_rewards, topN_votes)

    for idx, (author, permalink, title, filtered_body, reward, votes) in enumerate(iterable):
        rank = idx + 1
        quote = '>' + filtered_body[:QUOTE_MAX_LENGTH].replace('\n', ' ') + '...'
        title = tftf.replace_newlines(title)
        title = tftf.filter_special_characters(title)
        entry = topN_entry.format(rank=rank, author=author, permalink=permalink,
                                   title=title, quote=quote, votes=int(votes),
                                   reward=int(reward))
        result_string += entry
    return result_string


def topN_post(topN_authors, topN_permalinks, topN_titles,
               topN_filtered_bodies, topN_rewards, topN_votes, title_date,
               truffle_link=TRUFFLE_LINK, truffle_image=TRUFFLE_IMAGE,
               quote_max_length=QUOTE_MAX_LENGTH):

    title = """The daily Top 10 Truffle Picks: Find Quality Posts that deserve more Attention! ({date})"""

    post=""" ## Daily Truffle Picks
    
Good day dear beloved Steemit community! It's time for another round of truffles I found digging in the streams of this beautiful platform.

For those of you who do not know me: My name is *TrufflePig*. I am a bot based on Artificial Intelligence and Machine Learning to support minnows and help content curators. I was created and am being maintained by @smcaterpillar. I search for quality content that got less rewards than it deserves. I call these posts truffles and publish a daily top list. Now it is up to you to give these posts the attention they deserve. If you are curious how I select content, [you can find an explanation here.]({truffle_link})
    
Please, be aware that the list below has been automatically generated by a Machine Learning algorithm that was trained on payouts of previous contributions of the Steemit community. Of course, **this algorithm can make mistakes**. I try to draw attention to these posts and it is up to the Steemit community to decide whether these are really good contributions. I personally do not endorse any content, opinions, or political views found in these posts. In case you have problems with the compiled list or you have other feedback for me, leave a comment to help me improve.
    
# The Top 10 Truffles

Here are the top 10 posts that - according to my algorithm - deseve more reward and votes. The rank of a truffle is determined by the difference between current and my estimated rewards.

{topN_truffles}

#### You can Help and Contribute
By upvoting and resteeming the found truffles from above, you help minnows and promote good content on Steemit. By upvoting and resteeming this top list, you help covering the server costs and finance further development and improvement of my humble self. Alternativley, if you feel very generous you can delegate Steem Power to me and boost my daily upvotes on the truffle posts.

Cheers,

{truffle_image}

*`TrufflePig`*
    """

    topN_truffles = topN_list(topN_authors=topN_authors,
                               topN_permalinks=topN_permalinks,
                               topN_titles=topN_titles,
                               topN_filtered_bodies=topN_filtered_bodies,
                               topN_rewards=topN_rewards,
                               topN_votes=topN_votes,
                               quote_max_length=quote_max_length)

    title = title.format(date=title_date.strftime('%d.%m.%Y'))
    post = post.format(topN_truffles=topN_truffles,
                          truffle_image=truffle_image,
                          truffle_link=truffle_link)
    return title, post