<script>
  const gemsList = document.getElementById('gemsList');
  const filterInput = document.getElementById('filterState');
  let allGems = [];

  async function fetchGems() {
    try {
      const res = await fetch('/api/hidden-gems/all');
      const data = await res.json();
      allGems = data;
      renderGems(data);
    } catch (err) {
      gemsList.innerHTML = "❌ Error loading gems.";
      console.error(err);
    }
  }

  function renderGems(gems) {
    if (gems.length === 0) {
      gemsList.innerHTML = "⚠️ No hidden gems found.";
      return;
    }

    gemsList.innerHTML = "";
    gems.forEach(gem => {
      const div = document.createElement("div");
      div.classList.add("gem");

      div.innerHTML = `
        <h3>${gem.name} (${gem.state}) ${gem.approved ? '✅' : '🕒'}</h3>
        <p>${gem.description}</p>
        ${gem.image_url ? `<img src="${gem.image_url}" width="100" />` : ""}
        <small>Submitted by: ${gem.submitted_by}</small>
        <br/>
        ${!gem.approved ? `<button onclick="approveGem(${gem.id})">✅ Approve</button>` : ""}
        <button onclick="deleteGem(${gem.id})">🗑️ Delete</button>
      `;

      gemsList.appendChild(div);
    });
  }

  async function approveGem(id) {
    try {
      const res = await fetch(`/api/hidden-gems/approve/${id}`, {
        method: 'POST'
      });
      if (res.ok) {
        fetchGems();
      } else {
        alert('❌ Failed to approve');
      }
    } catch (err) {
      console.error(err);
    }
  }

  async function deleteGem(id) {
    if (!confirm("Are you sure you want to delete this gem?")) return;

    try {
      const res = await fetch(`/api/hidden-gems/delete/${id}`, {
        method: 'DELETE'
      });
      if (res.ok) {
        fetchGems();
      } else {
        alert('❌ Failed to delete');
      }
    } catch (err) {
      console.error(err);
    }
  }

  filterInput.addEventListener("input", () => {
    const keyword = filterInput.value.trim().toLowerCase();
    const filtered = allGems.filter(g => g.state.toLowerCase().includes(keyword));
    renderGems(filtered);
  });

  fetchGems();
</script>
