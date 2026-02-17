Screenshots folder — how to capture images for submission

Place your screenshots here using the filenames below so they match the links in `SUBMISSION_PROOF.md`.

Recommended filenames (use PNG):
- `branch_list.png` — Branch list output or screenshot
- `dockerhub_tags.png` — DockerHub repository page showing image tags

Commands to generate branch-list output (copy the output or screenshot it):

```bash
# Show branches local + remote (copy the output to a file or screenshot)
git branch -a

# Or capture a compact graph of commits and branches
git log --oneline --graph --all --decorate > branch_graph.txt
# Then open branch_graph.txt and take a screenshot of the terminal window
```

How to capture DockerHub tags (suggested):
1. Open your browser to: https://hub.docker.com/u/<your-dockerhub-username>
2. Click your repository (e.g., `nv23005ahmedkhalil/todo-app`).
3. Make sure the `Tags` view is visible and shows the image tags (e.g., `0.1.0`, `latest`).
4. Take a screenshot and save as `dockerhub_tags.png`.

Tips:
- On Linux you can use `gnome-screenshot` or `scrot`.
- On macOS press `Cmd+Shift+4` and select the area.
- On Windows use `Win+Shift+S` or the Snipping Tool.

Place the images in this folder and commit them. Then replace the placeholders in `SUBMISSION_PROOF.md` with the actual links/paths.
