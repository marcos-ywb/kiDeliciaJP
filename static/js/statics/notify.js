document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        const $notification = $delete.parentNode;

        const closeNotification = () => {
            if ($notification && $notification.parentNode) {
                $notification.style.opacity = '0';

                setTimeout(() => {
                    if ($notification.parentNode) {
                        $notification.parentNode.removeChild($notification);
                    }
                }, 500);
            }
        };

        const autoCloseTimeout = setTimeout(closeNotification, 5000);

        $delete.addEventListener('click', () => {
            clearTimeout(autoCloseTimeout);
            closeNotification();
        });
    });
});
