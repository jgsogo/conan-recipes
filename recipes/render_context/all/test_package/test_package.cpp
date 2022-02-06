#include <iostream>

#include "units/milimeters.hpp"
#include "units/pixels.hpp"
#include "render/imgui/context.h"

using namespace math::units;
using namespace render::imgui::units;

int main()
{
    std::cout << "Test render_context" << std::endl;

    ImGui::CreateContext();
    ImGuiIO &io = ImGui::GetIO();
    io.DisplaySize = ImVec2(1920, 1080);
    io.DeltaTime = 1.0f / 60.0f;

    // Build atlas
    unsigned char *tex_pixels = nullptr;
    int tex_w, tex_h;
    io.Fonts->GetTexDataAsRGBA32(&tex_pixels, &tex_w, &tex_h);

    ImGui::NewFrame();
    auto drawlist = ImGui::GetWindowDrawList();

    render::ImGuiContext<math::Milimeters::symbol> context{*drawlist};
    using Vector2Mm = Magnum::Math::Vector2<math::types::MilimetersT<float>>;

    // Draw circle
    Vector2Mm center{0_mm, 0_mm};
    context.drawCircle(center, 10_mm, IM_COL32_BLACK, 2_impx);

    ImGui::DestroyContext();
}
