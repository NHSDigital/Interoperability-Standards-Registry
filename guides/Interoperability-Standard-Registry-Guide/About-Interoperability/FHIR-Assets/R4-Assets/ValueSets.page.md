<label>
    <input type="checkbox" id="ukcore-checkbox" checked>
    Show UKCore Items
    </label>
    <br>
    <label>
    <input type="checkbox" id="nhsengland-checkbox" checked>
    Show NHSEngland Items
    </label>

    
<script>
    const ukcoreCheckbox = document.getElementById('ukcore-checkbox');
    const nhsenglandCheckbox = document.getElementById('nhsengland-checkbox');

    ukcoreCheckbox.addEventListener('change', function() {
        const ukcoreItems = document.querySelectorAll('.ukcore');
        ukcoreItems.forEach(item => {
        if (ukcoreCheckbox.checked) {
            item.classList.remove('hidden');
        } else {
            item.classList.add('hidden');
        }
        });
    });

    nhsenglandCheckbox.addEventListener('change', function() {
        const nhsenglandItems = document.querySelectorAll('.nhsengland');
        nhsenglandItems.forEach(item => {
        if (nhsenglandCheckbox.checked) {
            item.classList.remove('hidden');
        } else {
            item.classList.add('hidden');
        }
        });
    });
    </script>

    
## ValueSets

<div class="status-container">
<ul>

</ul></div><br><br>

---


