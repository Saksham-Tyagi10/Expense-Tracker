let chartInstance = null;

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('tx-date').valueAsDate = new Date();
  loadCategories();
  loadTransactions();

  document.getElementById('tx-form').addEventListener('submit', handleFormSubmit);
});

async function loadCategories() {
  const res = await fetch('/api/categories');
  const categories = await res.json();
  const select = document.getElementById('tx-category');
  select.innerHTML = categories.map(c => `<option value="${c.category_id}">${c.category_name}</option>`).join('');
}

async function loadTransactions() {
  const res = await fetch('/api/transactions');
  const transactions = await res.json();

  let income = 0, expense = 0;
  const tbody = document.getElementById('tx-table-body');
  tbody.innerHTML = '';

  const categoryExpenses = {};

  transactions.forEach(t => {
    const amt = parseFloat(t.amount);
    if (t.type === 'INCOME') {
      income += amt;
    } else {
      expense += amt;
      const cat = t.category_name || 'Other';
      categoryExpenses[cat] = (categoryExpenses[cat] || 0) + amt;
    }

    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${t.date}</td>
      <td><span class="badge bg-secondary">${t.category_name || '-'}</span></td>
      <td>${t.description || '-'}</td>
      <td><small class="text-muted">${t.payment_method || '-'}</small></td>
      <td class="fw-bold ${t.type === 'INCOME' ? 'text-success' : 'text-danger'}">
        ${t.type === 'INCOME' ? '+' : '-'}₹${amt.toFixed(2)}
      </td>
      <td>
        <button class="btn btn-sm btn-outline-danger" onclick="deleteTx(${t.transaction_id})">&times;</button>
      </td>
    `;
    tbody.appendChild(row);
  });

  document.getElementById('total-income').textContent = `₹${income.toFixed(2)}`;
  document.getElementById('total-expense').textContent = `₹${expense.toFixed(2)}`;
  document.getElementById('net-balance').textContent = `₹${(income - expense).toFixed(2)}`;

  updateChart(categoryExpenses);
}

async function handleFormSubmit(e) {
  e.preventDefault();
  const data = {
    type: document.getElementById('tx-type').value,
    category_id: parseInt(document.getElementById('tx-category').value),
    amount: parseFloat(document.getElementById('tx-amount').value),
    date: document.getElementById('tx-date').value,
    payment_method: document.getElementById('tx-method').value,
    description: document.getElementById('tx-desc').value
  };

  await fetch('/api/transactions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  document.getElementById('tx-desc').value = '';
  document.getElementById('tx-amount').value = '';
  loadTransactions();
}

async function deleteTx(id) {
  if (confirm('Delete this entry?')) {
    await fetch(`/api/transactions/${id}`, { method: 'DELETE' });
    loadTransactions();
  }
}

function updateChart(categoryData) {
  const ctx = document.getElementById('expenseChart').getContext('2d');
  const labels = Object.keys(categoryData);
  const data = Object.values(categoryData);

  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels.length ? labels : ['No Expense'],
      datasets: [{
        data: data.length ? data : [1],
        backgroundColor: ['#0d6efd', '#6610f2', '#6f42c1', '#d63384', '#dc3545', '#fd7e14', '#ffc107', '#198754']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
}
