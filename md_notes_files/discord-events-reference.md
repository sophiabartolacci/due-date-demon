# Discord Bot Events Reference

## Connection Events
```python
@client.event
async def on_ready():
    # Bot connected and ready - no parameters
    pass

@client.event  
async def on_disconnect():
    # Bot lost connection - no parameters
    pass
```

## Message Events
```python
@client.event
async def on_message(message):
    # Someone sent a message
    # message: discord.Message object
    # Contains: message.content, message.author, message.channel
    pass

@client.event
async def on_message_delete(message):
    # Message was deleted
    # message: discord.Message object (the deleted message)
    pass

@client.event
async def on_message_edit(before, after):
    # Message was edited
    # before: original message, after: edited message
    pass
```

## Member Events
```python
@client.event
async def on_member_join(member):
    # Someone joined the server
    # member: discord.Member object
    # Contains: member.name, member.guild, member.id
    pass

@client.event
async def on_member_remove(member):
    # Someone left the server
    # member: discord.Member object
    pass
```

## Reaction Events
```python
@client.event
async def on_reaction_add(reaction, user):
    # Someone added a reaction
    # reaction: discord.Reaction object
    # user: discord.User who added the reaction
    pass

@client.event
async def on_reaction_remove(reaction, user):
    # Someone removed a reaction
    # reaction: discord.Reaction object  
    # user: discord.User who removed the reaction
    pass
```

## Error Events
```python
@client.event
async def on_error(event, *args, **kwargs):
    # An error occurred
    # event: string name of the event that errored
    # *args, **kwargs: the arguments passed to the event
    pass
```

## Key Notes
- Parameter names are **fixed** by Discord.py - can't be changed
- All event functions must be `async def`
- Use `@client.event` decorator to register
- `on_ready()` is most common for simple bots