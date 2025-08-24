#include <furi.h>
#include <furi_hal.h>
#include <gui/gui.h>
#include <input/input.h>
#include <stdlib.h>

typedef struct {
    FuriMessageQueue* input_queue;
    bool running;
} AppState;

static void draw_callback(Canvas* canvas, void* ctx) {
    UNUSED(ctx);
    canvas_clear(canvas);
    canvas_set_font(canvas, FontPrimary);
    canvas_draw_str(canvas, 8, 20, "Spectrum Alert");
    canvas_set_font(canvas, FontSecondary);
    canvas_draw_str(canvas, 8, 40, "Waiting for GPIO/UART...");
}

static void input_callback(InputEvent* event, void* ctx) {
    AppState* app = ctx;
    if(event->type == InputTypeShort && event->key == InputKeyBack) {
        app->running = false;
    }
}

int32_t application_app(void* p) {
    UNUSED(p);
    AppState app = {.running = true};

    ViewPort* vp = view_port_alloc();
    view_port_draw_callback_set(vp, draw_callback, &app);
    view_port_input_callback_set(vp, input_callback, &app);

    Gui* gui = furi_record_open(RECORD_GUI);
    gui_add_view_port(gui, vp, GuiLayerFullscreen);

    // Configure GPIO pin (assumes a chosen pin is wired)
    // NOTE: Adjust pin based on your wiring; demo uses PC0 as placeholder.
    // furi_hal_gpio_init_simple(&gpio_pc0, GpioModeInput);

    while(app.running) {
        // Poll a GPIO or UART; on trigger, vibrate
        furi_hal_vibro_on(true);
        furi_delay_ms(50);
        furi_hal_vibro_on(false);
        furi_delay_ms(750);
        // In a real app, guard this behind an external signal condition.
        break;
    }

    gui_remove_view_port(gui, vp);
    view_port_free(vp);
    furi_record_close(RECORD_GUI);
    return 0;
}
