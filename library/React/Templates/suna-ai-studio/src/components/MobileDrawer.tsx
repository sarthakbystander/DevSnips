import { useEffect, useRef } from "react";
import { SidebarContent } from "./Sidebar";

interface MobileDrawerProps {
  open: boolean;
  onClose: () => void;
  onNewTrack: () => void;
}

export function MobileDrawer({
  open,
  onClose,
  onNewTrack,
}: MobileDrawerProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    if (open && !dialog.open) {
      dialog.showModal();
    } else if (!open && dialog.open) {
      dialog.close();
    }
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previous;
    };
  }, [open]);

  return (
    <dialog
      ref={dialogRef}
      className="drawer fixed left-0 top-0 m-0 h-[100dvh] max-h-none w-[86vw] max-w-[320px] overflow-hidden rounded-none border-0 bg-paper p-0 text-ink shadow-2xl"
      onClose={onClose}
      onCancel={(event) => {
        event.preventDefault();
        onClose();
      }}
      onClick={(event) => {
        if (event.target === event.currentTarget) onClose();
      }}
      aria-label="Session panel"
    >
      <SidebarContent
        onNewTrack={onNewTrack}
        onClose={onClose}
        onNavigate={onClose}
      />
    </dialog>
  );
}
