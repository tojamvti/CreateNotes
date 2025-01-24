from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory notes storage
notes = {}

# Home route to display all notes
@app.route('/')
def index():
    search_query = request.args.get('search', '')  # Get the search query if any
    filtered_notes = {id: note for id, note in notes.items() if search_query.lower() in note['title'].lower() or search_query.lower() in note['content'].lower()} if search_query else notes
    return render_template('index.html', notes=filtered_notes, search_query=search_query)

# Route to create a new note
@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_id = len(notes) + 1
        notes[note_id] = {'title': title, 'content': content}
        return redirect(url_for('index'))
    return render_template('create_note.html')

# Route to edit an existing note
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = notes.get(id)
    if not note:
        return redirect(url_for('index'))
    if request.method == 'POST':
        note['title'] = request.form['title']
        note['content'] = request.form['content']
        return redirect(url_for('index'))
    return render_template('create_note.html', note=note)

# Route to delete a note
@app.route('/delete/<int:id>', methods=['POST'])
def delete_note(id):
    if id in notes:
        del notes[id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
